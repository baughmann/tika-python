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

import csv
import tarfile
from collections.abc import Generator
from contextlib import closing
from http import HTTPStatus
from io import BytesIO, TextIOWrapper
from pathlib import Path
from sys import version_info
from typing import Any, BinaryIO

from tika.core import SERVER_ENDPOINT, TikaError, TikaResponse, call_server, parse_1


def from_file(
    file_obj: Path,
    *,
    server_endpoint: str = SERVER_ENDPOINT,
    request_options: dict[str, Any] | None = None,
) -> TikaResponse:
    """Parses a file using Apache Tika server's unpack endpoint.

    This function sends the provided file to a Tika server for parsing and returns
    the extracted content, metadata, and attachments.

    Args:
        file_obj: A Path object pointing to the file to be parsed.
        server_endpoint: The URL of the Tika server. Defaults to SERVER_ENDPOINT.
        request_options: Optional dictionary of request options to pass to the server.
            Can include parameters like timeout, headers, etc.

    Returns:
        TikaResponse: A dictionary-like object containing:
            - content: The extracted text content (str)
            - metadata: Dictionary of metadata key-value pairs
            - attachments: Dictionary of embedded files
            - status: HTTP status code of the response

    Raises:
        TikaError: If the server returns an unsuccessful status code or if parsing fails.
        FileNotFoundError: If the specified file does not exist.

    Example:
        >>> from pathlib import Path
        >>> response = from_file(Path("document.pdf"))
        >>> print(response.content)  # Print extracted text
        >>> print(response.metadata)  # Print document metadata
    """
    tar_output = parse_1(
        option="unpack",
        url_or_path=file_obj,
        server_endpoint=server_endpoint,
        response_mime_type="application/x-tar",
        services={"meta": "/meta", "text": "/tika", "all": "/rmeta/xml", "unpack": "/unpack/all"},
        raw_response=True,
        request_options=request_options,
    )
    return _parse(tar_output=tar_output)


def from_buffer(
    buf: str | bytes | BinaryIO,
    *,
    server_endpoint: str = SERVER_ENDPOINT,
    headers: dict[str, Any] | None = None,
    request_options: dict[str, Any] | None = None,
) -> TikaResponse:
    """Parses content directly from a buffer using Apache Tika server's unpack endpoint.

    This function sends buffered content (string, bytes, or file-like object) to a Tika
    server for parsing and returns the extracted content, metadata, and attachments.

    Args:
        buf: The content to be parsed. Can be:
            - str: Text content
            - bytes: Binary content
            - BinaryIO: File-like object containing binary content
        server_endpoint: The URL of the Tika server. Defaults to SERVER_ENDPOINT.
        headers: Optional dictionary of additional HTTP headers to send with the request.
            The 'Accept: application/x-tar' header will be added automatically.
        request_options: Optional dictionary of request options to pass to the server.
            Can include parameters like timeout, headers, etc.

    Returns:
        TikaResponse: A dictionary-like object containing:
            - content: The extracted text content (str)
            - metadata: Dictionary of metadata key-value pairs
            - attachments: Dictionary of embedded files
            - status: HTTP status code of the response

    Raises:
        TikaError: If the server returns an unsuccessful status code or if parsing fails.
        TypeError: If the input string is not of the correct type.

    Example:
        >>> with open("document.pdf", "rb") as f:
        ...     response = from_buffer(f.read())
        >>> print(response.metadata.get("Content-Type"))
    """

    headers = headers or {}
    headers.update({"Accept": "application/x-tar"})

    status, response = call_server(
        verb="put",
        server_endpoint=server_endpoint,
        service="/unpack/all",
        data=buf,
        headers=headers,
        verbose=False,
        raw_response=True,
        request_options=request_options,
    )

    if status != HTTPStatus.OK:
        msg = f"Unexpected response from Tika server ({status}): {response}"
        raise TikaError(msg)

    return _parse(tar_output=(status, response))


def _parse(tar_output: tuple[int, str | bytes | BinaryIO]) -> TikaResponse:  # noqa: C901
    """Parses a TAR file containing Tika server output into structured data.

    Internal function that processes the TAR file returned by Tika's unpack endpoint.
    Extracts metadata, content, and attachments from the TAR archive.

    Args:
        tar_output: A tuple containing:
            - status code (int)
            - TAR file content (str, bytes, or file-like object)

    Returns:
        TikaResponse: A dictionary-like object containing:
            - content: The extracted text content (str)
            - metadata: Dictionary of metadata key-value pairs
            - attachments: Dictionary of embedded files
            - status: Always 200 for successful parsing

    Raises:
        TikaError: If metadata or content extraction fails, or if the TAR file
            is malformed or missing required members.

    Note:
        This is an internal function that should not be called directly. Use
        from_file() or from_buffer() instead.
    """
    parsed = TikaResponse(
        status=200,
        metadata=None,
        content=None,
        attachments=None,
    )
    if not tar_output or tar_output[1] is None or tar_output[1] == b"":
        return parsed

    with tarfile.open(fileobj=BytesIO(tar_output[1])) as tar_file:  # type: ignore
        # get the member names
        member_names = list(tar_file.getnames())

        # extract the metadata
        metadata: dict[str, Any] = {}
        if "__METADATA__" in member_names:
            member_names.remove("__METADATA__")

        metadata_member = tar_file.getmember("__METADATA__")
        if not metadata_member.issym() and metadata_member.isfile():
            extracted = tar_file.extractfile(metadata_member)
            if not extracted:
                msg = "Failed to extract metadata from TAR file"
                raise TikaError(msg)
            if version_info.major >= 3:
                with closing(TextIOWrapper(extracted, encoding=tar_file.encoding)) as metadata_file:
                    metadata_reader = csv.reader(_truncate_nulls(metadata_file))
                    for metadata_line in metadata_reader:
                        # each metadata line comes as a key-value pair, with list values
                        # returned as extra values in the line - convert single values
                        # to non-list values to be consistent with parser metadata
                        if not len(metadata_line) >= 2:
                            msg = "Failed to extract metadata from TAR file"
                            raise TikaError(msg)

                        if len(metadata_line) > 2:
                            metadata[metadata_line[0]] = metadata_line[1:]
                        else:
                            metadata[metadata_line[0]] = metadata_line[1]
            else:
                extracted = tar_file.extractfile(metadata_member)
                if not extracted:
                    msg = "Failed to extract metadata from TAR file"
                    raise TikaError(msg)
                with closing(TextIOWrapper(extracted)) as metadata_file:
                    metadata_reader = csv.reader(_truncate_nulls(metadata_file))
                    for metadata_line in metadata_reader:
                        # each metadata line comes as a key-value pair, with list values
                        # returned as extra values in the line - convert single values
                        # to non-list values to be consistent with parser metadata
                        if len(metadata_line) < 2:
                            msg = "Failed to extract metadata from TAR file"
                            raise TikaError(msg)

                        if len(metadata_line) > 2:
                            metadata[metadata_line[0]] = metadata_line[1:]
                        else:
                            metadata[metadata_line[0]] = metadata_line[1]

        # get the content
        content: str = ""
        if "__TEXT__" in member_names:
            member_names.remove("__TEXT__")

            content_member = tar_file.getmember("__TEXT__")
            if not content_member.issym() and content_member.isfile():
                extracted = tar_file.extractfile(content_member)
                if not extracted:
                    msg = "Failed to extract content from TAR file"
                    raise TikaError(msg)
                if version_info.major >= 3:
                    with closing(TextIOWrapper(extracted, encoding="utf8")) as content_file:
                        content = content_file.read()
                else:
                    with closing(extracted) as content_file:
                        content = content_file.read().decode("utf8")

        # get the remaining files as attachments
        attachments: dict[str, Any] = {}
        for attachment in member_names:
            attachment_member = tar_file.getmember(attachment)
            if not attachment_member.issym() and attachment_member.isfile():
                extracted = tar_file.extractfile(attachment_member)
                if not extracted:
                    msg = "Failed to extract attachment from TAR file"
                    raise TikaError(msg)
                with closing(extracted) as attachment_file:
                    attachments[attachment] = attachment_file.read()

        parsed["content"] = content
        parsed["metadata"] = metadata
        parsed["attachments"] = attachments

        return parsed


# TODO: Remove if/when fixed. https://issues.apache.org/jira/browse/TIKA-3070
def _truncate_nulls(s: list[str] | TextIOWrapper) -> Generator[Any, Any, None]:
    for line in s:
        yield line.replace("\0", "")
