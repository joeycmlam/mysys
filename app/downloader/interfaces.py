from abc import ABC, abstractmethod
from typing import Dict, Optional
from .config import FactsheetConfig

class IDownloader(ABC):
    """Interface for file downloaders."""
    
    @abstractmethod
    def download(self, url: str, output_path: str) -> bool:
        """Download a file from URL to the specified path."""
        pass