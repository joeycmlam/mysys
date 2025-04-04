import logging
import requests
from pathlib import Path
from typing import Dict, Optional
from config import Config, FactsheetConfig

class FactsheetDownloader:
    """Downloads factsheets from specified URLs."""
    
    def __init__(self, config: Config):
        self.config = config
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        logging.basicConfig(
            level=self.config.get_log_level(),
            format=self.config.get_log_format()
        )
        self.logger = logging.getLogger(__name__)
    
    def _generate_filename(self, factsheet: FactsheetConfig) -> str:
        """Generate a filename for the downloaded factsheet."""
        output_dir = Path(factsheet.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        return str(output_dir / f"{factsheet.name}.pdf")
    
    def download_factsheet(self, factsheet: FactsheetConfig) -> Optional[str]:
        """Download a factsheet from the specified URL."""
        try:
            filename = self._generate_filename(factsheet)
            self.logger.info(f"Downloading factsheet '{factsheet.name}' from {factsheet.url}")
            
            # Download the file
            response = requests.get(factsheet.url, stream=True)
            response.raise_for_status()
            
            # Save the file
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            self.logger.info(f"Successfully downloaded factsheet '{factsheet.name}' to {filename}")
            return filename
            
        except requests.RequestException as e:
            self.logger.error(f"Error downloading factsheet '{factsheet.name}': {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error downloading factsheet '{factsheet.name}': {str(e)}")
            return None
    
    def download_all_factsheets(self) -> Dict[str, Optional[str]]:
        """Download all configured factsheets."""
        results = {}
        for factsheet in self.config.get_factsheets():
            results[factsheet.name] = self.download_factsheet(factsheet)
        return results 