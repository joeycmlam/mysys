import json
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass
from urllib.parse import urlparse
from config import Config


@dataclass
class DownloadConfig:
    """Configuration for downloading a single file."""
    url: str
    output_dir: str
    name: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DownloadConfig':
        """Create a DownloadConfig instance from a dictionary."""
        required_fields = {'url', 'output_dir'}
        missing_fields = required_fields - set(data.keys())
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Generate name from URL if not provided
        name = data.get('name', '')
        if not name:
            url_path = urlparse(data['url']).path
            name = Path(url_path).stem  # Get filename without extension

        return cls(
            url=data['url'],
            output_dir=data['output_dir'],
            name=name
        )


class DownloaderConfig(Config):
    """Configuration manager for the downloader."""

    def __init__(self, config_path: str):
        """Initialize the downloader configuration."""
        super().__init__(config_path)
        self.files: List[DownloadConfig] = []
        self._load_files()

    def _load_files(self) -> None:
        """Load file configurations."""
        files_config = self.settings.get('files', [])
        if not files_config:
            raise ValueError("No file configurations found in config file")

        self.files = [DownloadConfig.from_dict(config) for config in files_config]

    def get_files_list(self) -> List[DownloadConfig]:
        """Get all factsheet configurations."""
        return self.files
    


