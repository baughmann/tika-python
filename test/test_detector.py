import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import BinaryIO, cast

import pytest

import tika

# Test constants
TEST_FILES = {
    "txt": ("plain.txt", "Hello world", "text/plain"),
    "html": ("page.html", "<html><body>Hello</body></html>", "text/html"),
    "json": ("data.json", '{"key": "value"}', "application/json"),
    "xml": ("config.xml", "<?xml version='1.0'?><root></root>", "application/xml"),
}


@pytest.fixture
def sample_files() -> Generator[dict[str, Path], None, None]:
    """Create temporary files of different types for MIME detection."""
    files: dict[str, Path] = {}

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for ext, (filename, content, _) in TEST_FILES.items():
            file_path = temp_path / filename
            file_path.write_text(content, encoding="utf-8")
            files[ext] = file_path

        yield files


async def test_detect_from_file_path_str(sample_files: dict[str, Path]) -> None:
    """Test MIME type detection from file using string path."""
    result = await tika.detector.from_file(str(sample_files["txt"]))
    assert isinstance(result, str | bytes)
    result_str = result if isinstance(result, str) else result.decode()
    assert "text/plain" in result_str.lower()


async def test_detect_from_file_path_object(sample_files: dict[str, Path]) -> None:
    """Test MIME type detection from file using Path object."""
    result = await tika.detector.from_file(sample_files["html"])
    assert isinstance(result, str | bytes)
    result_str = result if isinstance(result, str) else result.decode()
    assert "text/html" in result_str.lower()


async def test_detect_from_binary_file() -> None:
    """Test MIME type detection from binary file object."""
    content = TEST_FILES["json"][1]
    with tempfile.NamedTemporaryFile(mode="w+b", suffix=".json") as temp_file:
        temp_file.write(content.encode("utf-8"))
        temp_file.flush()
        temp_file.seek(0)

        result = await tika.detector.from_file(cast(BinaryIO, temp_file))
        assert isinstance(result, str | bytes)
        result_str = result if isinstance(result, str) else result.decode()
        assert "application/json" in result_str.lower()


async def test_detect_from_buffer_str() -> None:
    """Test MIME type detection from string buffer."""
    result = await tika.detector.from_buffer(TEST_FILES["xml"][1])
    assert isinstance(result, str | bytes)
    result_str = result if isinstance(result, str) else result.decode()
    assert "application/xml" in result_str.lower()


async def test_detect_from_buffer_bytes() -> None:
    """Test MIME type detection from bytes buffer."""
    content = TEST_FILES["html"][1].encode("utf-8")
    result = await tika.detector.from_buffer(content)
    assert isinstance(result, str | bytes)
    result_str = result if isinstance(result, str) else result.decode()
    assert "text/html" in result_str.lower()


async def test_detect_with_config_path(sample_files: dict[str, Path]) -> None:
    """Test MIME type detection with custom config path."""
    config_path = "/path/to/config"
    result = await tika.detector.from_file(sample_files["txt"], config_path=config_path)
    assert isinstance(result, str | bytes)


async def test_detect_with_request_options() -> None:
    """Test MIME type detection with custom request options."""
    options = {"timeout": 30}
    result = await tika.detector.from_buffer(TEST_FILES["json"][1], request_options=options)
    assert isinstance(result, str | bytes)


@pytest.mark.parametrize(
    ("ext", "filename", "content", "expected_type"),
    [(ext, data[0], data[1], data[2]) for ext, data in TEST_FILES.items()],
)
async def test_mime_type_detection_accuracy(
    ext: str,
    filename: str,
    content: str,
    expected_type: str,
    tmp_path: Path,
) -> None:
    """Test accuracy of MIME type detection for various file types."""
    # Create actual file with content
    file_path = tmp_path / filename
    file_path.write_text(content)

    # Test with actual file
    result = await tika.detector.from_file(file_path)
    assert isinstance(result, str | bytes)
    result_str = result if isinstance(result, str) else result.decode()
    assert expected_type == result_str.casefold()


@pytest.mark.parametrize(
    "invalid_input",
    [
        "",  # Empty string
        " ",  # Whitespace only
        "\n\n",  # Just newlines
    ],
)
async def test_detect_edge_cases(invalid_input: str) -> None:
    """Test MIME type detection with edge cases."""
    result = await tika.detector.from_buffer(invalid_input)
    assert isinstance(result, str | bytes)
