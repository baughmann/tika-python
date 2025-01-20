import tempfile
from pathlib import Path
from typing import Generator
from urllib.request import urlretrieve

import pytest

# Constants
TEST_IMAGE_URL = "https://placehold.co/4000x4000.jpg"
MIN_FILE_SIZE = 10000  # bytes


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


def test_image_download(temp_dir: Path) -> None:
    """Test downloading and verifying a large image file."""
    image_path = temp_dir / "pic.jpg"
    urlretrieve(TEST_IMAGE_URL, image_path)

    assert image_path.exists(), "Downloaded image file should exist"
    assert image_path.stat().st_size > MIN_FILE_SIZE, "Image file should be larger than minimum size"
