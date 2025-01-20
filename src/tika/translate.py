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

from tika.tika import SERVER_ENDPOINT, TRANSLATOR, call_server, do_translate_1


def from_file(
    file_obj: str | Path | BinaryIO,
    srcLang: str,
    destLang: str,
    server_endpoint: str = SERVER_ENDPOINT,
    request_options: dict[str, Any] | None = None,
) -> str | bytes | BinaryIO:
    """
    Translates the content of source file to destination language
    :param filename: file whose contents needs translation
    :param srcLang: name of language of input file
    :param destLang: name of language of desired language
    :param server_endpoint: Tika server end point (Optional)
    :return: translated content
    """
    _, response = do_translate_1(
        option=srcLang + ":" + destLang,
        urlOrPath=file_obj,
        server_endpoint=server_endpoint,
        request_options=request_options,
    )
    return response


def from_buffer(
    buf: str | bytes | BinaryIO,
    srcLang: str,
    destLang: str,
    server_endpoint: str = SERVER_ENDPOINT,
    request_options: dict[str, Any] | None = None,
) -> str | bytes | BinaryIO:
    """
    Translates content from source language to desired destination language
    :param string: input content which needs translation
    :param srcLang: name of language of the input content
    :param destLang: name of the desired language for translation
    :param server_endpoint:
    :return:
    """
    _, response = call_server(
        verb="put",
        server_endpoint=server_endpoint,
        service="/translate/all/" + TRANSLATOR + "/" + srcLang + "/" + destLang,
        data=buf,
        headers={"Accept": "text/plain"},
        verbose=False,
        request_options=request_options,
    )
    return response


def auto_from_file(
    file_obj: str | Path | BinaryIO,
    destLang: str,
    server_endpoint: str = SERVER_ENDPOINT,
    request_options: dict[str, Any] | None = None,
) -> str | bytes | BinaryIO:
    """
    Translates contents of a file to desired language by auto detecting the source language
    :param filename: file whose contents needs translation
    :param destLang: name of the desired language for translation
    :param server_endpoint: Tika server end point (Optional)
    :return:
    """
    _, response = do_translate_1(
        option=destLang,
        urlOrPath=file_obj,
        server_endpoint=server_endpoint,
        request_options=request_options,
    )
    return response


def auto_from_buffer(
    buf: str | bytes | BinaryIO,
    destLang: str,
    server_endpoint: str = SERVER_ENDPOINT,
    request_options: dict[str, Any] | None = None,
) -> str | bytes | BinaryIO:
    """
    Translates content to desired language by auto detecting the source language
    :param string: input content which needs translation
    :param destLang: name of the desired language for translation
    :param server_endpoint: Tika server end point (Optional)
    :return:
    """
    _, response = call_server(
        verb="put",
        server_endpoint=server_endpoint,
        service="/translate/all/" + TRANSLATOR + "/" + destLang,
        data=buf,
        headers={"Accept": "text/plain"},
        verbose=False,
        request_options=request_options,
    )
    return response
