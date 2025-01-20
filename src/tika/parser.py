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
    """Parse a file for metadata and content.

    :param obj: Path to file or binary file object (opened with 'rb')
    :param server_endpoint: Server endpoint URL
    :param service: Service requested from the tika server:
        - 'all' (default): Returns recursive text content + metadata
        - 'meta': Returns only metadata
        - 'text': Returns only content
    :param xml_content: Whether to request XML content (False returns text)
    :param headers: Optional request headers for tika server
    :param config_path: Optional path to configuration file
    :param request_options: Optional additional request options

    :return: TikaResponse containing metadata and content
    :rtype: TikaResponse
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
    """Parse content from a buffer.

    Args:
        buf: Buffer containing content to parse.
        server_endpoint: Optional server endpoint URL.
        xml_content: Whether XML content should be requested.
            Defaults to False which results in text content.
        headers: Optional request headers to be sent to the tika reset server.
        config_path: Optional path to configuration file.
        request_options: Optional additional request options.

    Returns:
        TikaResponse: Contains metadata and content keys.
            content: String value of parsed content.
            metadata: Dictionary of metadata values.

    Raises:
        TikaError: If the server returns a non-OK status code.
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
    """Parse response from Tika REST API server.

    Args:
        output: Tuple containing status code and raw content from server.
        service: Type of service requested ('all', 'meta', or 'text').
            Defaults to 'all'.

    Returns:
        TikaResponse: Contains metadata and content from parsed response.
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
