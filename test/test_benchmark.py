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

import zlib
from http import HTTPStatus
from pathlib import Path

from pytest_benchmark.fixture import BenchmarkFixture

import tika.parser
from test.utils import gzip_compress
from tika.tika import TikaResponse

# Type aliases
Headers = dict[str, str] | None

# Constants
TEST_FILES_DIR = Path(__file__).parent / "files"
TEST_PDF_PATH = TEST_FILES_DIR / "rwservlet.pdf"
GZIP_HEADERS = {"Accept-Encoding": "gzip, deflate"}


def tika_from_buffer_zlib(file: Path | str, headers: Headers = None) -> TikaResponse:
    """Process file with zlib compression."""
    with open(file, mode="rb") as file_obj:
        return tika.parser.from_buffer(zlib.compress(file_obj.read()), headers=headers)


def tika_from_buffer_gzip(file: Path | str, headers: Headers = None) -> TikaResponse:
    """Process file with gzip compression."""
    with open(file, mode="rb") as file_obj:
        return tika.parser.from_buffer(buf=gzip_compress(file_obj.read()), headers=headers)


def tika_from_buffer(file: Path | str, headers: Headers = None) -> TikaResponse:
    """Process file from buffer."""
    with open(file, mode="r") as file_obj:
        return tika.parser.from_buffer(buf=file_obj.read(), headers=headers)


def tika_from_binary(file: Path | str, headers: Headers = None) -> TikaResponse:
    """Process file from binary."""
    with open(file, mode="rb") as file_obj:
        return tika.parser.from_file(obj=file_obj, headers=headers)


def test_local_binary(benchmark: BenchmarkFixture) -> None:
    """Benchmark parsing file binary."""
    response = benchmark(tika_from_binary, TEST_PDF_PATH)
    assert response["status"] == HTTPStatus.OK


def test_parser_buffer(benchmark: BenchmarkFixture) -> None:
    """Benchmark parsing from buffer."""
    response = benchmark(tika_from_buffer, TEST_PDF_PATH)
    assert response["status"] == HTTPStatus.OK


def test_parser_buffer_zlib_input(benchmark: BenchmarkFixture) -> None:
    """Benchmark parsing with zlib compression."""
    response = benchmark(tika_from_buffer_zlib, TEST_PDF_PATH)
    assert response["status"] == HTTPStatus.OK


def test_parser_buffer_gzip_input(benchmark: BenchmarkFixture) -> None:
    """Benchmark parsing with gzip compression."""
    response = benchmark(tika_from_buffer_gzip, TEST_PDF_PATH)
    assert response["status"] == HTTPStatus.OK


def test_local_binary_with_gzip_output(benchmark: BenchmarkFixture) -> None:
    """Benchmark parsing binary with gzip output."""
    response = benchmark(tika_from_binary, TEST_PDF_PATH, headers=GZIP_HEADERS)
    assert response["status"] == HTTPStatus.OK


def test_parser_buffer_with_gzip_output(benchmark: BenchmarkFixture) -> None:
    """Benchmark parsing from buffer with gzip output."""
    response = benchmark(tika_from_buffer, TEST_PDF_PATH, headers=GZIP_HEADERS)
    assert response["status"] == HTTPStatus.OK


def test_parser_buffer_zlib_input_and_gzip_output(benchmark: BenchmarkFixture) -> None:
    """Benchmark parsing with zlib compression and gzip output."""
    response = benchmark(tika_from_buffer_zlib, TEST_PDF_PATH, headers=GZIP_HEADERS)
    assert response["status"] == HTTPStatus.OK


def test_parser_buffer_gzip_input_and_gzip_output(benchmark: BenchmarkFixture) -> None:
    """Benchmark parsing with gzip compression and output."""
    response = benchmark(tika_from_buffer_gzip, TEST_PDF_PATH, headers=GZIP_HEADERS)
    assert response["status"] == HTTPStatus.OK
