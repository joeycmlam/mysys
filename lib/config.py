import json
from pathlib import Path
from typing import Dict, Any

class Config:
    """Configuration manager for the factsheet downloader."""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.settings: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> None:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key."""
        return self.settings.get(key, default)
    
    def get_factsheet_url(self) -> str:
        """Get the factsheet URL from configuration."""
        url = self.get('factsheet', {}).get('url')
        if not url:
            raise ValueError("Factsheet URL not found in configuration")
        return url
    
    def get_output_dir(self) -> str:
        """Get the output directory from configuration."""
        output_dir = self.get('factsheet', {}).get('output_dir')
        if not output_dir:
            raise ValueError("Output directory not found in configuration")
        return output_dir
    
    def get_base_name(self) -> str:
        """Get the base filename from configuration."""
        base_name = self.get('factsheet', {}).get('base_name')
        if not base_name:
            raise ValueError("Base filename not found in configuration")
        return base_name
    
    def get_log_level(self) -> str:
        """Get the log level from configuration."""
        return self.get('logging', {}).get('level', 'INFO')
    
    def get_log_format(self) -> str:
        """Get the log format from configuration."""
        return self.get('logging', {}).get('format', '%(asctime)s - %(levelname)s - %(message)s') 