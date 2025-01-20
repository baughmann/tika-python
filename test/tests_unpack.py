# coding=utf8
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Generator

import pytest

from tika import unpack

# Test data
TEST_TEXT_UTF8 = "Hello, world!! 😎 👽"
TEST_TEXT_ASCII = "Hello, world!!"
TEST_TEMP_DIR = "/tmp"


@pytest.fixture
def utf8_file() -> Generator[Path, unpack.Any, None]:
    """Create a temporary file with UTF-8 encoded content."""
    with NamedTemporaryFile("w+b", prefix="tika-python", suffix=".txt", dir=TEST_TEMP_DIR, delete=False) as f:
        f.write(TEST_TEXT_UTF8.encode("utf8"))
        f.flush()
        f.seek(0)
        file_path = Path(f.name)

    yield file_path
    file_path.unlink()  # Cleanup after test


@pytest.fixture
def ascii_file() -> Generator[Path, unpack.Any, None]:
    """Create a temporary file with ASCII content."""
    with NamedTemporaryFile("w+t", prefix="tika-python", suffix=".txt", dir=TEST_TEMP_DIR, delete=False) as f:
        f.write(TEST_TEXT_ASCII)
        f.flush()
        f.seek(0)
        file_path = Path(f.name)

    yield file_path
    file_path.unlink()  # Cleanup after test


def test_utf8(utf8_file: Path) -> None:
    """Test unpacking a UTF-8 encoded file."""
    parsed = unpack.from_file(utf8_file)
    assert parsed["content"] is not None
    assert parsed["content"].strip() == TEST_TEXT_UTF8


def test_ascii(ascii_file: Path) -> None:
    """Test unpacking an ASCII encoded file."""
    parsed = unpack.from_file(ascii_file)
    assert parsed["content"] is not None
    assert parsed["content"].strip() == TEST_TEXT_ASCII


def test_from_buffer() -> None:
    """Test unpacking content from a buffer."""
    parsed = unpack.from_buffer("what?")
    assert parsed["metadata"] is not None
    assert parsed["metadata"]["Content-Length"] == "5"


def test_from_buffer_with_headers() -> None:
    """Test unpacking content from a buffer with custom headers."""
    parsed = unpack.from_buffer("what?", headers={"Param": "whatever"})
    assert parsed["metadata"] is not None
    assert parsed["metadata"]["Content-Length"] == "5"
