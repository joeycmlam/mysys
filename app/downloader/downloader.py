import logging
import requests
from pathlib import Path
from typing import Dict, Optional
from urllib.parse import urlparse
from config import Config, DownloadConfig


class FileDownloader:
    """Downloads factsheets from specified URLs."""

    def __init__(self, config):
        self.config = config
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        logging.basicConfig(
            level=self.config.get_log_level(),
            format=self.config.get_log_format()
        )
        self.logger = logging.getLogger(__name__)

    def download_file(self, dnfile: DownloadConfig) -> Optional[str]:
        """Download a factsheet from the specified URL."""
        try:
            # Create output directory
            output_dir = Path(dnfile.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            # Get original filename from URL
            url_path = urlparse(dnfile.url).path
            filename = str(output_dir / Path(url_path).name)

            self.logger.info(f"Downloading factsheet '{dnfile.name}' from {dnfile.url}")

            # Download the file
            response = requests.get(dnfile.url, stream=True)
            response.raise_for_status()

            # Save the file
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            self.logger.info(f"Successfully downloaded file '{dnfile.name}' to {filename}")
            return filename

        except requests.RequestException as e:
            self.logger.error(f"Error downloading file '{dnfile.name}': {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error downloading file '{dnfile.name}': {str(e)}")
            return None

