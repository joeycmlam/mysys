import logging
from typing import Dict, Optional
from config import Config, FactsheetConfig
from file_utils import FileUtils

class FactsheetDownloader(IFactsheetDownloader):
    """Downloads factsheets from specified URLs."""
    
    def __init__(self, config: Config, downloader: Optional[IDownloader] = None):
        self.config = config
        self.downloader = downloader
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        logging.basicConfig(
            level=self.config.get_log_level(),
            format=self.config.get_log_format()
        )
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def download_factsheet(self, factsheet: FactsheetConfig) -> Optional[str]:
        """Download a factsheet from the specified URL."""
        try:
            # Create output directory
            output_dir = FileUtils.create_output_dir(factsheet.output_dir)
            
            # Get filename and create full path
            filename = FileUtils.get_filename_from_url(factsheet.url)
            output_path = output_dir / filename
            
            self.logger.info(f"Downloading factsheet '{factsheet.name}' from {factsheet.url}")
            
            # Download the file
            if self.downloader.download(factsheet.url, str(output_path)):
                self.logger.info(f"Successfully downloaded factsheet '{factsheet.name}' to {output_path}")
                return str(output_path)
            return None
            
        except Exception as e:
            self.logger.error(f"Error processing factsheet '{factsheet.name}': {str(e)}")
            return None
    
    def download_all_factsheets(self) -> Dict[str, Optional[str]]:
        """Download all configured factsheets."""
        results = {}
        for factsheet in self.config.get_factsheets():
            results[factsheet.name] = self.download_factsheet(factsheet)
        return results 