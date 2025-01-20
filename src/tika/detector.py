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
from typing import Any, BinaryIO

from tika.core import SERVER_ENDPOINT, TikaError, call_server, detect_type_1


async def from_file(
    file_obj: str | Path | BinaryIO,
    *,
    config_path: str | None = None,
    request_options: dict[str, Any] | None = None,
) -> str | bytes | BinaryIO:
    """Detects the MIME type of a file using Apache Tika server.

    Analyzes the file content to determine its MIME type (media type) using Tika's
    detection capabilities. This is more reliable than extension-based detection.

    Args:
        file_obj: The file to analyze. Can be:
            - str: A file path or URL
            - Path: A pathlib.Path object pointing to the file
            - BinaryIO: A file-like object in binary read mode
        config_path: Optional path to a custom Tika configuration file.
        request_options: Optional dictionary of request options to pass to the server.
            Can include parameters like timeout, headers, etc.

    Returns:
        The detected MIME type (e.g., 'application/pdf', 'image/jpeg').
        Return type matches the server response, which may be str, bytes, or BinaryIO.

    Raises:
        TikaError: If the server returns an unsuccessful status code or if type
            detection fails.
        FileNotFoundError: If the specified file does not exist.

    Example:
        >>> from pathlib import Path
        >>> mime_type = from_file(Path("document.pdf"))
        >>> print(mime_type)  # Prints 'application/pdf'
        >>> mime_type = from_file("image.jpg")
        >>> print(mime_type)  # Prints 'image/jpeg'
    """
    status, response = await detect_type_1(
        option="type",
        url_or_path=file_obj,
        config_path=config_path,
        request_options=request_options,
    )
    if status != HTTPStatus.OK:
        msg = f"Unexpected response from Tika server ({status}): {response}"
        raise TikaError(msg)
    return response


async def from_buffer(
    buf: str | bytes | BinaryIO,
    *,
    config_path: str | None = None,
    request_options: dict[str, Any] | None = None,
) -> str | bytes | BinaryIO:
    """Detects the MIME type of content provided in a buffer using Apache Tika server.

    Analyzes the buffered content to determine its MIME type (media type) using
    Tika's detection capabilities. Useful for content that hasn't been saved to
    a file or for streaming data.

    Args:
        buf: The content to analyze. Can be:
            - str: Text content
            - bytes: Binary content
            - BinaryIO: File-like object containing binary content
        config_path: Optional path to a custom Tika configuration file.
        request_options: Optional dictionary of request options to pass to the server.
            Can include parameters like timeout, headers, etc.

    Returns:
        The detected MIME type (e.g., 'application/pdf', 'text/plain').
        Return type matches the server response, which may be str, bytes, or BinaryIO.

    Raises:
        TikaError: If the server returns an unsuccessful status code or if type
            detection fails.
        TypeError: If the input buffer is not of the correct type.

    Example:
        >>> with open("document.pdf", "rb") as f:
        ...     mime_type = from_buffer(f.read())
        >>> print(mime_type)  # Prints 'application/pdf'

        >>> text_content = "Hello, world!"
        >>> mime_type = from_buffer(text_content)
        >>> print(mime_type)  # Prints 'text/plain'
    """
    status, response = await call_server(
        verb="put",
        server_endpoint=SERVER_ENDPOINT,
        service="/detect/stream",
        data=buf,
        headers={"Accept": "text/plain"},
        verbose=False,
        config_path=config_path,
        request_options=request_options,
    )
    if status != HTTPStatus.OK:
        msg = f"Unexpected response from Tika server ({status}): {response}"
        raise TikaError(msg)

    return response
