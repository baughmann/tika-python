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

from unittest.mock import patch

import pytest

import tika
from tika import TikaResponse

# Test data constants
TEST_PDF_URL = "https://boe.es/boe/dias/2019/12/02/pdfs/BOE-A-2019-17288.pdf"
EXPECTED_CONTENT_SNIPPET = "AUTORIDADES Y PERSONAL"
EXPECTED_CONTENT_TYPE = "application/pdf"


@pytest.fixture
async def pdf_parse_result() -> TikaResponse:
    """Fixture to get parse results for the test PDF."""
    return await tika.parser.from_file(TEST_PDF_URL)


async def test_default_service(pdf_parse_result: TikaResponse) -> None:
    """Test parsing file using default service."""
    assert pdf_parse_result["metadata"]
    assert pdf_parse_result["metadata"]["Content-Type"] == EXPECTED_CONTENT_TYPE
    assert pdf_parse_result["content"]
    assert isinstance(pdf_parse_result["content"], str)
    assert EXPECTED_CONTENT_SNIPPET in pdf_parse_result["content"]


async def test_remote_endpoint() -> None:
    """Test parsing with a remote Tika endpoint."""
    with patch("tika.parser.parse_1") as tika_call_mock, patch("tika.parser._parse"):
        await tika.parser.from_file("filename", server_endpoint="http://tika:9998/tika")

        tika_call_mock.assert_called_once_with(
            option="all",
            url_or_path="filename",
            server_endpoint="http://tika:9998/tika",
            headers=None,
            config_path=None,
            request_options=None,
        )


async def test_default_service_explicit(pdf_parse_result: TikaResponse) -> None:
    """Test parsing file using default service with explicit 'all' parameter."""
    result = await tika.parser.from_file(TEST_PDF_URL, service="all")
    assert result["metadata"]
    assert result["metadata"]["Content-Type"] == EXPECTED_CONTENT_TYPE
    assert result["content"]
    assert isinstance(result["content"], str)
    assert EXPECTED_CONTENT_SNIPPET in result["content"]


async def test_text_service() -> None:
    """Test parsing file using the content-only service."""
    result = await tika.parser.from_file(TEST_PDF_URL, service="text")
    assert result["metadata"] is None
    assert result["content"]
    assert isinstance(result["content"], str)
    assert EXPECTED_CONTENT_SNIPPET in result["content"]


async def test_meta_service() -> None:
    """Test parsing file using the metadata-only service."""
    result = await tika.parser.from_file(TEST_PDF_URL, service="meta")
    assert result["content"] is None
    assert result["metadata"]
    assert result["metadata"]["Content-Type"] == EXPECTED_CONTENT_TYPE


async def test_invalid_service() -> None:
    """Test parsing file using an invalid service falls back to default parsing."""
    result = await tika.parser.from_file(TEST_PDF_URL, service="bad")
    assert result["metadata"]
    assert result["metadata"]["Content-Type"] == EXPECTED_CONTENT_TYPE
    assert result["content"]
    assert isinstance(result["content"], str)
    assert EXPECTED_CONTENT_SNIPPET in result["content"]
