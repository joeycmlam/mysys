import logging
import requests
from typing import Dict, Optional
from config import Config
from downloadConfig import DownloadConfig, DownloaderConfig
from file_utils import FileUtils


class FileDownloader:
    """Downloads files from specified URLs."""

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
        """Download a file from the specified URL."""
        try:
            # Create output directory
            FileUtils.create_output_dir(dnfile.output_dir)

            # Get original filename from URL
            filename = FileUtils.get_filename_from_url(dnfile.url)

            self.logger.info(f"Downloading file '{dnfile.name}' from {dnfile.url}")

            # Download the file
            response = requests.get(dnfile.url, stream=True)
            response.raise_for_status()

            # Save the file
            output_path = dnfile.output_dir + "/" + filename
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            self.logger.info(f"Successfully downloaded file '{dnfile.name}' to {output_path}")
            return filename

        except requests.RequestException as e:
            self.logger.error(f"Error downloading file '{dnfile.name}': {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error downloading file '{dnfile.name}': {str(e)}")
            return None
