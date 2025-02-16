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

import zlib
from pathlib import Path

import pytest
from memory_profiler import profile

import tika
from test.utils import gzip_compress

# Constants
TEST_FILES_DIR = Path(__file__).parent / "files"
TEST_PDF_PATH = TEST_FILES_DIR / "rwservlet.pdf"
GZIP_HEADERS = {"Accept-Encoding": "gzip, deflate"}


@pytest.mark.benchmark
@profile
async def test_parser_binary() -> None:
    """Profile memory usage when parsing binary file directly."""
    with open(TEST_PDF_PATH, "rb") as file_obj:
        response = await tika.parser.from_file(file_obj, headers=GZIP_HEADERS)
        assert response is not None
        assert response["status"] == 200
        assert response["content"] is not None


@pytest.mark.benchmark
@profile
async def test_parser_buffer() -> None:
    """Profile memory usage when parsing from buffer."""
    with open(TEST_PDF_PATH) as file_obj:
        response = await tika.parser.from_buffer(file_obj.read(), headers=GZIP_HEADERS)
        assert response is not None
        assert response["status"] == 200
        assert response["content"] is not None


@pytest.mark.benchmark
@profile
async def test_parser_zlib() -> None:
    """Profile memory usage when parsing with zlib compression."""
    with open(TEST_PDF_PATH, "rb") as file_obj:
        response = await tika.parser.from_buffer(zlib.compress(file_obj.read()), headers=GZIP_HEADERS)
        assert response is not None
        assert response["status"] == 200
        assert response["content"] is not None


@pytest.mark.benchmark
@profile
async def test_parser_gzip() -> None:
    """Profile memory usage when parsing with gzip compression."""
    with open(TEST_PDF_PATH, "rb") as file_obj:
        response = await tika.parser.from_buffer(gzip_compress(file_obj.read()), headers=GZIP_HEADERS)
        assert response is not None
        assert response["status"] == 200
        assert response["content"] is not None
