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
