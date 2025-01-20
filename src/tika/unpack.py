#!/usr/bin/env python
# encoding: utf-8
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
from contextlib import closing
from http import HTTPStatus
from io import BytesIO, TextIOWrapper
from pathlib import Path
from sys import version_info
from typing import Any, BinaryIO, Generator

from tika.core import SERVER_ENDPOINT, TikaException, TikaResponse, call_server, parse_1


def from_file(
    filename: Path,
    server_endpoint: str = SERVER_ENDPOINT,
    request_options: dict[str, Any] | None = None,
) -> TikaResponse:
    """
    Parse from file
    :param filename: file
    :param server_endpoint: Tika server end point (optional)
    :return:
    """
    tarOutput = parse_1(
        option="unpack",
        urlOrPath=filename,
        server_endpoint=server_endpoint,
        responseMimeType="application/x-tar",
        services={"meta": "/meta", "text": "/tika", "all": "/rmeta/xml", "unpack": "/unpack/all"},
        rawResponse=True,
        request_options=request_options,
    )
    return _parse(tarOutput=tarOutput)


def from_buffer(
    string: str | bytes | BinaryIO,
    server_endpoint: str = SERVER_ENDPOINT,
    headers: dict[str, Any] | None = None,
    request_options: dict[str, Any] | None = None,
) -> TikaResponse:
    """
    Parse from buffered content
    :param string:  buffered content
    :param server_endpoint: Tika server URL (Optional)
    :return: parsed content
    """

    headers = headers or {}
    headers.update({"Accept": "application/x-tar"})

    status, response = call_server(
        verb="put",
        server_endpoint=server_endpoint,
        service="/unpack/all",
        data=string,
        headers=headers,
        verbose=False,
        rawResponse=True,
        request_options=request_options,
    )

    if status != HTTPStatus.OK:
        raise TikaException(f"Unexpected response from Tika server ({status}): {response}")

    return _parse(tarOutput=(status, response))


def _parse(tarOutput) -> TikaResponse:
    parsed = TikaResponse(
        status=200,
        metadata=None,
        content=None,
        attachments=None,
    )
    if not tarOutput:
        return parsed
    elif tarOutput[1] is None or tarOutput[1] == b"":
        return parsed

    with tarfile.open(fileobj=BytesIO(tarOutput[1])) as tarFile:
        # get the member names
        memberNames = list(tarFile.getnames())

        # extract the metadata
        metadata: dict[str, Any] = {}
        if "__METADATA__" in memberNames:
            memberNames.remove("__METADATA__")

        metadataMember = tarFile.getmember("__METADATA__")
        if not metadataMember.issym() and metadataMember.isfile():
            extracted = tarFile.extractfile(metadataMember)
            if not extracted:
                raise TikaException("Failed to extract metadata from TAR file")
            if version_info.major >= 3:
                with closing(TextIOWrapper(extracted, encoding=tarFile.encoding)) as metadataFile:
                    metadataReader = csv.reader(_truncate_nulls(metadataFile))
                    for metadataLine in metadataReader:
                        # each metadata line comes as a key-value pair, with list values
                        # returned as extra values in the line - convert single values
                        # to non-list values to be consistent with parser metadata
                        assert len(metadataLine) >= 2

                        if len(metadataLine) > 2:
                            metadata[metadataLine[0]] = metadataLine[1:]
                        else:
                            metadata[metadataLine[0]] = metadataLine[1]
            else:
                extracted = tarFile.extractfile(metadataMember)
                if not extracted:
                    raise TikaException("Failed to extract metadata from TAR file")
                with closing(TextIOWrapper(extracted)) as metadataFile:
                    metadataReader = csv.reader(_truncate_nulls(metadataFile))
                    for metadataLine in metadataReader:
                        # each metadata line comes as a key-value pair, with list values
                        # returned as extra values in the line - convert single values
                        # to non-list values to be consistent with parser metadata
                        assert len(metadataLine) >= 2

                        if len(metadataLine) > 2:
                            metadata[metadataLine[0]] = metadataLine[1:]
                        else:
                            metadata[metadataLine[0]] = metadataLine[1]

        # get the content
        content: str = ""
        if "__TEXT__" in memberNames:
            memberNames.remove("__TEXT__")

            contentMember = tarFile.getmember("__TEXT__")
            if not contentMember.issym() and contentMember.isfile():
                extracted = tarFile.extractfile(contentMember)
                if not extracted:
                    raise TikaException("Failed to extract content from TAR file")
                if version_info.major >= 3:
                    with closing(TextIOWrapper(extracted, encoding="utf8")) as content_file:
                        content = content_file.read()
                else:
                    with closing(extracted) as content_file:
                        content = content_file.read().decode("utf8")

        # get the remaining files as attachments
        attachments: dict[str, Any] = {}
        for attachment in memberNames:
            attachmentMember = tarFile.getmember(attachment)
            if not attachmentMember.issym() and attachmentMember.isfile():
                extracted = tarFile.extractfile(attachmentMember)
                if not extracted:
                    raise TikaException("Failed to extract attachment from TAR file")
                with closing(extracted) as attachment_file:
                    attachments[attachment] = attachment_file.read()

        parsed["content"] = content
        parsed["metadata"] = metadata
        parsed["attachments"] = attachments

        return parsed


# TODO: Remove if/when fixed. https://issues.apache.org/jira/browse/TIKA-3070
def _truncate_nulls(s) -> Generator[Any, Any, None]:
    for line in s:
        yield line.replace("\0", "")
