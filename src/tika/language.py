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

from tika.core import SERVER_ENDPOINT, TikaError, call_server, detect_lang_1


async def from_file(
    file_obj: str | Path | BinaryIO,
    request_options: dict[str, Any] | None = None,
) -> str | bytes | BinaryIO:
    """Detects the language of a file using Apache Tika server.

    Uses Tika's language detection capabilities to identify the primary language
    of text content within a file.

    Args:
        file_obj: The file to analyze. Can be:
            - str: A string path to the file
            - Path: A pathlib.Path object pointing to the file
            - BinaryIO: A file-like object in binary read mode
        request_options: Optional dictionary of request options to pass to the server.
            Can include parameters like timeout, headers, etc.

    Returns:
        The detected language code (e.g., 'en' for English, 'fr' for French).
        Return type matches the server response, which may be str, bytes, or BinaryIO.

    Raises:
        TikaError: If the server returns an unsuccessful status code or if language
            detection fails.
        FileNotFoundError: If the specified file does not exist.

    Example:
        >>> from pathlib import Path
        >>> language = from_file(Path("document.txt"))
        >>> print(language)  # Prints 'en' for English text
    """
    status, response = await detect_lang_1(option="file", url_or_path=file_obj, request_options=request_options)
    if status != HTTPStatus.OK:
        msg = f"Unexpected response from Tika server ({status}): {response}"
        raise TikaError(msg)
    return response


async def from_buffer(
    buf: str | bytes | BinaryIO,
    request_options: dict[str, Any] | None = None,
) -> str | bytes | BinaryIO:
    """Detects the language of content provided in a buffer using Apache Tika server.

    Sends the buffered content directly to Tika's language detection service
    to identify the primary language of the text.

    Args:
        buf: The content to analyze. Can be:
            - str: Text content as a string
            - bytes: Binary content
            - BinaryIO: File-like object containing content
        request_options: Optional dictionary of request options to pass to the server.
            Can include parameters like timeout, headers, etc.

    Returns:
        The detected language code (e.g., 'en' for English, 'fr' for French).
        Return type matches the server response, which may be str, bytes, or BinaryIO.

    Raises:
        TikaError: If the server returns an unsuccessful status code or if language
            detection fails.
        TypeError: If the input buffer is not of the correct type.

    Example:
        >>> text = "Bonjour le monde!"
        >>> language = from_buffer(text)
        >>> print(language)  # Prints 'fr' for French text
    """
    status, response = await call_server(
        verb="put",
        server_endpoint=SERVER_ENDPOINT,
        service="/language/string",
        data=buf,
        headers={"Accept": "text/plain"},
        verbose=False,
        request_options=request_options,
    )
    if status != HTTPStatus.OK:
        msg = f"Unexpected response from Tika server ({status}): {response}"
        raise TikaError(msg)
    return response
