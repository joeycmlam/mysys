import logging
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional
from config import Config

class FactsheetDownloader:
    """Downloads factsheet PDFs from a configured URL."""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the downloader with configuration.
        
        Args:
            config: Optional Config instance. If not provided, creates a new one.
        """
        self.config = config or Config()
        self._setup_logging()
        self.logger = logging.getLogger(__name__)
    
    def _setup_logging(self) -> None:
        """Configure logging based on config settings."""
        logging.basicConfig(
            level=self.config.get_log_level(),
            format=self.config.get_log_format()
        )
    
    def _generate_filename(self) -> str:
        """Generate a unique filename with timestamp."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{self.config.get_base_name()}_{timestamp}.pdf"
    
    def download(self) -> Optional[Path]:
        """
        Download the factsheet from the configured URL.
        
        Returns:
            Path to the downloaded file if successful, None otherwise
        """
        try:
            # Get URL from config
            url = self.config.get_factsheet_url()
            if not url:
                self.logger.error("No factsheet URL configured")
                return None
            
            # Create output directory
            output_dir = Path(self.config.get_output_dir())
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate output path
            filename = self._generate_filename()
            output_path = output_dir / filename
            
            # Download the file
            self.logger.info(f"Downloading factsheet from {url}")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Save the file
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            self.logger.info(f"Factsheet downloaded successfully to {output_path}")
            return output_path
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error downloading factsheet: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return None 