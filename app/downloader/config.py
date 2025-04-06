import json
from pathlib import Path
from typing import Dict, Any

class Config:
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self._validate_config_path()
        self.settings = self._load_config()
        self._validate_settings()
    
    def _validate_config_path(self) -> None:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        if not self.config_path.is_file():
            raise ValueError(f"Configuration path is not a file: {self.config_path}")
    
    def _load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON configuration in {self.config_path}: {e}")
    
    def _validate_settings(self) -> None:
        if not self.settings:
            raise ValueError("Empty configuration file")
    
    def get_log_level(self) -> str:
        return self.settings.get('logging', {}).get('level', 'INFO')
    
    def get_log_format(self) -> str:
        return self.settings.get('logging', {}).get('format', '%(asctime)s - %(levelname)s - %(message)s')
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

