from abc import ABC, abstractmethod
from typing import Dict, Optional
from .config import FactsheetConfig

class IDownloader(ABC):
    """Interface for file downloaders."""
    
    @abstractmethod
    def download(self, url: str, output_path: str) -> bool:
        """Download a file from URL to the specified path."""
        pass

class IFactsheetDownloader(ABC):
    """Interface for factsheet downloaders."""
    
    @abstractmethod
    def download_factsheet(self, factsheet: FactsheetConfig) -> Optional[str]:
        """Download a factsheet from the specified URL."""
        pass
    
    @abstractmethod
    def download_all_factsheets(self) -> Dict[str, Optional[str]]:
        """Download all configured factsheets."""
        pass 