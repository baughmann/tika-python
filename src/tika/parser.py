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
    """
    Parses a file for metadata and content
    :param filename: path to file which needs to be parsed or binary file using open(path,'rb')
    :param server_endpoint: Server endpoint url
    :param service: service requested from the tika server
                    Default is 'all', which results in recursive text content+metadata.
                    'meta' returns only metadata
                    'text' returns only content
    :param xml_content: Whether or not XML content be requested.
                    Default is 'False', which results in text content.
    :param headers: Request headers to be sent to the tika reset server, should
                    be a dictionary. This is optional
    :return: dictionary having 'metadata' and 'content' keys.
            'content' has a str value and metadata has a dict type value.
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
    """
    Parses the content from buffer
    :param string: Buffer value
    :param server_endpoint: Server endpoint. This is optional
    :param xml_content: Whether or not XML content be requested.
                    Default is 'False', which results in text content.
    :param headers: Request headers to be sent to the tika reset server, should
                    be a dictionary. This is optional
    :return:
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
    """Parse response from Tika REST API server."""
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
