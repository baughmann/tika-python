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
from collections.abc import Generator
from http import HTTPStatus
from pathlib import Path
from typing import BinaryIO

import pytest

import tika

# Constants
TEST_FILES_DIR = Path(__file__).parent / "files"
TEST_PDF_PATH = TEST_FILES_DIR / "rwservlet.pdf"


async def test_remote_pdf() -> None:
    """Test parsing a remote PDF file."""
    result = await tika.parser.from_file(
        "http://appsrv.achd.net/reports/rwservlet?food_rep_insp&P_ENCOUNTER=201504160015"
    )
    assert result is not None


async def test_remote_html() -> None:
    """Test parsing a remote HTML file."""
    result = await tika.parser.from_file("http://neverssl.com/index.html")
    assert result is not None


async def test_remote_mp3() -> None:
    """Test parsing a remote MP3 file."""
    result = await tika.parser.from_file("https://archive.org/download/Ainst-Spaceshipdemo.mp3/Ainst-Spaceshipdemo.mp3")
    assert result is not None


async def test_remote_jpg() -> None:
    """Test parsing a remote JPG file."""
    result = await tika.parser.from_file("https://placehold.co/600x400.jpg")
    assert result is not None


@pytest.fixture
def pdf_file() -> Generator[BinaryIO, None, None]:
    """Fixture providing a test PDF file object."""
    with open(TEST_PDF_PATH, "rb") as file_obj:
        yield file_obj


async def test_local_binary(pdf_file: BinaryIO) -> None:
    """Test parsing a local binary file."""
    result = await tika.parser.from_file(pdf_file)
    assert result is not None


async def test_local_buffer() -> None:
    """Test parsing text from a buffer."""
    result = await tika.parser.from_buffer("Good evening, Dave")
    assert result["status"] == HTTPStatus.OK


async def test_local_path() -> None:
    """Test parsing a local file path."""
    result = await tika.parser.from_file(TEST_PDF_PATH)
    assert result is not None


async def test_kill_server(pdf_file: BinaryIO) -> None:
    """Test parsing a file and then killing the server."""
    await tika.parser.from_file(pdf_file)
    result = tika.kill_server()
    assert result is None
