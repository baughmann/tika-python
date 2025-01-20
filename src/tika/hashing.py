import hashlib
import logging
from pathlib import Path

import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_sha1(sha1_source: str | Path) -> str | None:
    """
    Get SHA1 hash from either a local file or URL.

    Args:
        sha1_source: Can be:
            - Path object pointing to local file
            - String filepath to local file
            - URL string starting with http:// or https://

    Returns:
        The SHA1 string if successful, None if fails
    """
    # Convert string paths to Path objects
    if isinstance(sha1_source, str) and not sha1_source.startswith(("http://", "https://")):
        sha1_source = Path(sha1_source)

    # Handle local files (both Path and converted string paths)
    if isinstance(sha1_source, Path):
        try:
            with open(sha1_source) as f:
                return f.read().strip()
        except OSError as e:
            logger.error(f"Failed to read SHA1 file: {e}")
            return None

    # Handle URLs
    try:
        response = requests.get(sha1_source, timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except requests.ConnectionError:
        logger.warning("Unable to reach server - are you offline?")
        return None
    except requests.RequestException as e:
        logger.error(f"Failed to download SHA1: {e}")
        return None


def compute_file_sha1(file_path: Path) -> str | None:
    """Compute SHA1 hash of a file."""
    try:
        sha1 = hashlib.sha1()  # noqa: S324 - the best tika provides is sha1

        with open(file_path, "rb") as f:
            while chunk := f.read(8192):  # 8KB chunks
                sha1.update(chunk)

        return sha1.hexdigest()
    except OSError as e:
        logger.error(f"Failed to read file: {e}")
        return None


def verify_jar_sha1(jar_path: Path, sha1_source: str | Path) -> bool:
    """
    Verify JAR file against its SHA1 hash from either a local file or URL.

    Args:
        jar_path: Path to the JAR file to verify
        sha1_source: Path, filepath, or URL to get the SHA1 from

    Returns:
        True if verification succeeds, False otherwise
    """
    expected_sha1 = get_sha1(sha1_source)
    if not expected_sha1:
        return False

    actual_sha1 = compute_file_sha1(jar_path)
    if not actual_sha1:
        return False

    return expected_sha1 == actual_sha1
