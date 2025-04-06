import logging
import requests
from pathlib import Path
from typing import Optional

class HttpDownloader():
    """HTTP implementation of the downloader interface."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(self.__class__.__name__)
    
    def download(self, url: str, output_path: str) -> bool:
        """Download a file from URL to the specified path."""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
            
        except requests.RequestException as e:
            self.logger.error(f"Error downloading file: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return False 