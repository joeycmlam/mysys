from pathlib import Path
from urllib.parse import urlparse
from typing import Optional


class FileUtils:
    """Utility class for file operations."""

    @staticmethod
    def get_filename_from_url(url: str) -> str:
        """Extract filename from URL."""
        url_path = urlparse(url).path
        return Path(url_path).name

    @staticmethod
    def create_output_dir(output_dir: str) -> Path:
        """Create output directory if it doesn't exist."""
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path
