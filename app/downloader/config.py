import json
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass
from urllib.parse import urlparse

@dataclass
class FactsheetConfig:
    """Configuration for a single factsheet."""
    url: str
    output_dir: str
    name: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FactsheetConfig':
        """Create a FactsheetConfig instance from a dictionary."""
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
                raise ValueError("No factsheet configurations found in config file")
            
            self.factsheets = [FactsheetConfig.from_dict(config) for config in factsheet_configs]
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON configuration: {e}")
    
    def get_factsheets(self) -> List[FactsheetConfig]:
        """Get all factsheet configurations."""
        return self.factsheets
    
    def get_factsheet_by_name(self, name: str) -> FactsheetConfig:
        """Get a specific factsheet configuration by name."""
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