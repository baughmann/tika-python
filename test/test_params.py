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

# Reference
# https://docs.python.org/2/library/unittest.html
# http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases
# public domain license reference: http://eli.thegreenplace.net/pages/code

import csv
from pathlib import Path

import pytest

import tika


def load_test_urls() -> list[str]:
    """Load test URLs from CSV file."""
    csv_path = Path(__file__).parent / "arguments" / "test_remote_content.csv"

    with open(csv_path) as csvfile:
        urls = [row[1] for row in csv.reader(csvfile)]
        return urls[1:]  # Skip header row


@pytest.fixture(params=load_test_urls())
def test_url(request: pytest.FixtureRequest) -> str:
    """Fixture providing test URLs from the CSV file."""
    return request.param


def test_parse_response_exists(test_url: str) -> None:
    """Test that parsing returns a response."""
    result = tika.parser.from_file(test_url)
    assert result is not None


def test_parse_metadata_exists(test_url: str) -> None:
    """Test that parsing returns metadata."""
    result = tika.parser.from_file(test_url)
    assert result["metadata"] is not None


def test_parse_content_exists(test_url: str) -> None:
    """Test that parsing returns content."""
    result = tika.parser.from_file(test_url)
    assert result["content"] is not None
