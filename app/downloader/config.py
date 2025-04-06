import json
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass
from urllib.parse import urlparse


class Config:
    """Base configuration manager."""
    
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self._validate_config_path()
        self.settings = self._load_config()
        self._validate_settings()
    
    def _validate_config_path(self) -> None:
        """Validate that the config file exists."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        if not self.config_path.is_file():
            raise ValueError(f"Configuration path is not a file: {self.config_path}")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON configuration in {self.config_path}: {e}")
    
    def _validate_settings(self) -> None:
        """Validate the configuration settings."""
        if not self.settings:
            raise ValueError("Empty configuration file")
    
    def get_log_level(self) -> str:
        """Get the log level."""
        return self.settings.get('logging', {}).get('level', 'INFO')
    
    def get_log_format(self) -> str:
        """Get the log format."""
        return self.settings.get('logging', {}).get('format', '%(asctime)s - %(levelname)s - %(message)s')
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)
    
    def get(self, key, default=None):
        return self.config_data.get(key, default)

