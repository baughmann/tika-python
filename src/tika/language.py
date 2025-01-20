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

from pathlib import Path
from typing import Any, BinaryIO

from tika.tika import SERVER_ENDPOINT, call_server, detect_lang_1


def from_file(filename: Path, request_options: dict[str, Any] | None = None) -> str | bytes | BinaryIO:
    """
    Detects language of the file
    :param filename: path to file whose language needs to be detected
    :return:
    """
    _, content = detect_lang_1(option="file", urlOrPath=filename, request_options=request_options)
    return content


def from_buffer(string, request_options: dict[str, Any] | None = None) -> str | bytes | BinaryIO:
    """
    Detects language of content in the buffer
    :param string: buffered data
    :return:
    """
    _, response = call_server(
        verb="put",
        server_endpoint=SERVER_ENDPOINT,
        service="/language/string",
        data=string,
        headers={"Accept": "text/plain"},
        verbose=False,
        request_options=request_options,
    )
    return response
