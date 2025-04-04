import json
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass
from urllib.parse import urlparse
from downloaderConfig import FactsheetConfig

class Config:
    """Configuration manager for the factsheet downloader."""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            current_file = Path(__file__).resolve()
            config_path = current_file.parent / "config.json"
        
        self.config_path = Path(config_path)
        self.settings: Dict[str, Any] = {}
        self.factsheets: List[FactsheetConfig] = []
        self.load()
    
    def load(self) -> None:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                self.settings = json.load(f)
            
            # Load factsheet configurations
            factsheet_configs = self.settings.get('factsheets', [])
            if not factsheet_configs:
                raise ValueError("No configurations found in config file")
            
            self.factsheets = [FactsheetConfig.from_dict(config) for config in factsheet_configs]
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON configuration: {e}")
    
    def get_factsheets(self) -> List[FactsheetConfig]:
        """Get all factsheet configurations."""
        return self.factsheets
    
    def get_factsheet_by_name(self, name: str) -> FactsheetConfig:
        """Get a specific configuration by name."""
        for factsheet in self.factsheets:
            if factsheet.name == name:
                return factsheet
        raise ValueError(f"Factsheet configuration not found: {name}")
    
    def get_log_level(self) -> str:
        """Get the log level from configuration."""
        return self.settings.get('logging', {}).get('level', 'INFO')
    
    def get_log_format(self) -> str:
        """Get the log format from configuration."""
        return self.settings.get('logging', {}).get('format', '%(asctime)s - %(levelname)s - %(message)s') 