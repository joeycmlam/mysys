import json
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass
from urllib.parse import urlparse
from downloadConfig import DownloadConfig


class Config:
    """Configuration manager for the downloader."""

    def __init__(self, config_file: str = None):
        if config_file is None:
            current_path = Path(__file__).resolve()
            config_file = current_path / "config.json"

        self.config_file = Path(config_file)
        self.settings: Dict[str, Any] = {}
        self.files: List[DownloadConfig] = []
        self.load()

    def load(self) -> None:
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                self.settings = json.load(f)

            # Load configurations
            factsheet_configs = self.settings.get('files', [])
            if not factsheet_configs:
                raise ValueError("No configurations found in config file")

            self.files = [DownloadConfig.from_dict(config) for config in factsheet_configs]

        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON configuration: {e}")

    def get_files_list(self) -> List[DownloadConfig]:
        """Get all factsheet configurations."""
        return self.files

    def get_factsheet_by_name(self, name: str) -> DownloadConfig:
        """Get a specific configuration by name."""
        for factsheet in self.files:
            if factsheet.name == name:
                return factsheet
        raise ValueError(f"Factsheet configuration not found: {name}")

    def get_log_level(self) -> str:
        """Get the log level from configuration."""
        return self.settings.get('logging', {}).get('level', 'INFO')

    def get_log_format(self) -> str:
        """Get the log format from configuration."""
        return self.settings.get('logging', {}).get('format', '%(asctime)s - %(levelname)s - %(message)s')
