import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import Any, BinaryIO, cast

import pytest

import tika

# Test constants
TEST_TEXTS = {
    "en": "The quick brown fox jumps over the lazy dog",  # English
    "es": "El rápido zorro marrón salta sobre el perro perezoso",  # Spanish
    "de": "Der schnelle braune Fuchs springt über den faulen Hund",  # German
}


@pytest.fixture
def sample_files() -> Generator[dict[str, Path], Any, None]:
    """Create temporary files with sample texts for language detection."""
    files: dict[str, Path] = {}

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for lang_code, text in TEST_TEXTS.items():
            file_path = temp_path / f"text_{lang_code}.txt"
            file_path.write_text(text, encoding="utf-8")
            files[lang_code] = file_path

        yield files


def test_detect_from_file_path_str(sample_files: dict[str, Path]) -> None:
    """Test language detection from file using string path."""
    result = tika.language.from_file(str(sample_files["en"]))
    assert isinstance(result, str | bytes)


def test_detect_from_file_path_object(sample_files: dict[str, Path]) -> None:
    """Test language detection from file using Path object."""
    result = tika.language.from_file(sample_files["es"])
    assert isinstance(result, str | bytes)


def test_detect_from_binary_file() -> None:
    """Test language detection from binary file object."""
    with tempfile.NamedTemporaryFile(mode="w+b") as temp_file:
        temp_file.write(TEST_TEXTS["de"].encode("utf-8"))
        temp_file.flush()
        temp_file.seek(0)

        result = tika.language.from_file(cast(BinaryIO, temp_file))
        assert isinstance(result, str | bytes)


def test_detect_from_buffer_str() -> None:
    """Test language detection from string buffer."""
    result = tika.language.from_buffer(TEST_TEXTS["en"])
    assert isinstance(result, str | bytes)


def test_detect_from_buffer_bytes() -> None:
    """Test language detection from bytes buffer."""
    text_bytes = TEST_TEXTS["es"].encode("utf-8")
    result = tika.language.from_buffer(text_bytes)
    assert isinstance(result, str | bytes)


def test_detect_with_request_options() -> None:
    """Test language detection with custom request options."""
    options = {"timeout": 30}
    result = tika.language.from_buffer(TEST_TEXTS["de"], request_options=options)
    assert isinstance(result, str | bytes)


@pytest.mark.parametrize(
    "invalid_input",
    [
        "",  # Empty string
        " ",  # Whitespace only
        "123",  # Numbers only
    ],
)
def test_detect_edge_cases(invalid_input: str) -> None:
    """Test language detection with edge cases."""
    result = tika.language.from_buffer(invalid_input)
    assert isinstance(result, str | bytes)
