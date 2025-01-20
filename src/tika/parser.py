#!/usr/bin/env python
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from http import HTTPStatus
from pathlib import Path
from typing import Any, BinaryIO, cast

import orjson

from tika.core import SERVER_ENDPOINT, TikaError, TikaResponse, call_server, parse_1


def from_file(
    obj: str | Path | BinaryIO,
    *,
    server_endpoint: str = SERVER_ENDPOINT,
    service: str = "all",
    xml_content: bool = False,
    headers: dict[str, Any] | None = None,
    config_path: str | None = None,
    request_options: dict[str, Any] | None = None,
) -> TikaResponse:
    """Parses a file using Apache Tika server and returns structured content and metadata.

    This function sends a file to the Tika server for parsing using the specified service
    and configuration options. It can handle local files, URLs, or binary streams.

    Args:
        obj: The file to be parsed. Can be:
            - str: A file path or URL
            - Path: A pathlib.Path object pointing to a file
            - BinaryIO: A file-like object in binary read mode
        server_endpoint: The URL of the Tika server. Defaults to SERVER_ENDPOINT.
        service: The Tika service to use. Must be one of:
            - "all": Both content and metadata (default)
            - "meta": Only metadata
            - "text": Only text content
        xml_content: If True, requests XML output instead of plain text.
            This affects how the content is structured in the response.
        headers: Additional HTTP headers to include in the request.
        config_path: Path to a custom Tika configuration file.
        request_options: Additional options for the HTTP request (e.g., timeout).

    Returns:
        TikaResponse: A dictionary-like object containing:
            - content: Extracted text or XML content (str or None)
            - metadata: Dictionary of document metadata (dict or None)
            - status: HTTP status code (int)
            - attachments: Any embedded files (dict or None)

    Raises:
        TikaError: If the server returns an error or parsing fails
        FileNotFoundError: If the specified file doesn't exist
        ValueError: If an invalid service type is specified

    Example:
        >>> response = from_file("document.pdf", service="all")
        >>> print(response.content)  # Print extracted text
        >>> print(response.metadata.get("Content-Type"))  # Get document type
    """
    if not xml_content:
        output = parse_1(
            option=service,
            url_or_path=obj,
            server_endpoint=server_endpoint,
            headers=headers,
            config_path=config_path,
            request_options=request_options,
        )
    else:
        output = parse_1(
            option=service,
            url_or_path=obj,
            server_endpoint=server_endpoint,
            services={"meta": "/meta", "text": "/tika", "all": "/rmeta/xml"},
            headers=headers,
            config_path=config_path,
            request_options=request_options,
        )
    return _parse(output=output, service=service)


def from_buffer(
    buf: str | bytes | BinaryIO,
    *,
    server_endpoint: str = SERVER_ENDPOINT,
    xml_content: bool = False,
    headers: dict[str, Any] | None = None,
    config_path: str | None = None,
    request_options: dict[str, Any] | None = None,
) -> TikaResponse:
    """Parses content directly from a buffer using Apache Tika server.

    This function sends buffered content to the Tika server for parsing and returns
    structured content and metadata. It automatically uses the /rmeta endpoint for
    either text or XML output.

    Args:
        buf: The content to parse. Can be:
            - str: Text content
            - bytes: Binary content
            - BinaryIO: File-like object with binary content
        server_endpoint: The URL of the Tika server. Defaults to SERVER_ENDPOINT.
        xml_content: If True, requests XML output instead of plain text.
            Affects the structure of the returned content.
        headers: Additional HTTP headers to include in the request.
            'Accept: application/json' is automatically added.
        config_path: Path to a custom Tika configuration file.
        request_options: Additional options for the HTTP request (e.g., timeout).

    Returns:
        TikaResponse: A dictionary-like object containing:
            - content: Extracted text or XML content (str or None)
            - metadata: Dictionary of document metadata (dict or None)
            - status: HTTP status code (int)
            - attachments: Any embedded files (dict or None)

    Raises:
        TikaError: If the server returns a non-200 status code or parsing fails
        TypeError: If the buffer is not of a supported type

    Example:
        >>> with open("document.pdf", "rb") as f:
        ...     response = from_buffer(f.read())
        >>> print(response.metadata)  # Print all metadata
    """
    headers = headers or {}
    headers.update({"Accept": "application/json"})

    if not xml_content:
        status, response = call_server(
            verb="put",
            server_endpoint=server_endpoint,
            service="/rmeta/text",
            data=buf,
            headers=headers,
            verbose=False,
            config_path=config_path,
            request_options=request_options,
        )
    else:
        status, response = call_server(
            verb="put",
            server_endpoint=server_endpoint,
            service="/rmeta/xml",
            data=buf,
            headers=headers,
            verbose=False,
            config_path=config_path,
            request_options=request_options,
        )

    if status != HTTPStatus.OK:
        msg = f"Unexpected response from Tika server ({status}): {response}"
        raise TikaError(msg)

    return _parse((status, response))


def _parse(output: tuple[int, str | bytes | BinaryIO | None], service: str = "all") -> TikaResponse:  # noqa: C901
    """Parses the raw response from Tika server into a structured format.

    Internal function that processes the raw response from Tika's REST API and
    converts it into a structured TikaResponse object. Handles different response
    formats based on the service type used.

    Args:
        output: A tuple containing:
            - HTTP status code (int)
            - Raw response content (str, bytes, BinaryIO, or None)
        service: The type of service that was requested. Must be one of:
            - "all": Both content and metadata (default)
            - "meta": Only metadata
            - "text": Only text content

    Returns:
        TikaResponse: A dictionary-like object containing:
            - content: Extracted text or XML content (str or None)
            - metadata: Dictionary of document metadata (dict or None)
            - status: HTTP status code (int)
            - attachments: Any embedded files (dict or None)

    Notes:
        - For 'text' service, the raw content is returned directly in the content field
        - For 'meta' service, the JSON response is parsed into the metadata field
        - For 'all' service, both content and metadata are extracted from the response
        - Handles complex metadata cases where values can be either strings or lists
        - This is an internal function that should not be called directly
    """
    status, raw_content = output
    parsed = TikaResponse(metadata=None, content=None, status=status, attachments=None)

    if not raw_content:
        return parsed

    if service == "text":
        parsed["content"] = raw_content
        return parsed

    raw_json: dict[str, Any] | list[dict[str, Any]] = orjson.loads(
        raw_content if not isinstance(raw_content, BinaryIO) else raw_content.read()
    )

    parsed["metadata"] = {}
    if service == "meta" and isinstance(raw_json, dict):
        for key, value in raw_json.items():
            if isinstance(value, str | list):
                parsed["metadata"][key] = cast(str | list[str], value)
        return parsed

    content: list[str] = []
    if isinstance(raw_json, list):
        for js in raw_json:
            if "X-TIKA:content" in js and isinstance(js["X-TIKA:content"], str):
                content.append(js["X-TIKA:content"])

        parsed["content"] = "".join(content) if content else None

        metadata_dict = parsed["metadata"]
        if metadata_dict is not None:
            for js in raw_json:
                for key, value in js.items():
                    if key != "X-TIKA:content":
                        current_value = metadata_dict.get(key)

                        if current_value is not None:
                            if isinstance(current_value, str):
                                metadata_dict[key] = [current_value]

                            if isinstance(value, str):  # noqa: SIM102
                                if isinstance(metadata_dict[key], list):
                                    cast(list[str], metadata_dict[key]).append(value)
                        else:
                            if isinstance(value, str | list):
                                metadata_dict[key] = cast(str | list[str], value)

    return parsed
