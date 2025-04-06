import logging
import argparse
from pathlib import Path
from typing import Dict, List
from downloadConfig import DownloaderConfig
from downloader import FileDownloader


class FactsheetDownloaderApp:
    """Main application class for downloading factsheets."""

    def __init__(self, config_file: str = None):
        self.config = DownloaderConfig(config_file)
        self._setup_logging()
        self.logger = logging.getLogger(__name__)

    def _setup_logging(self) -> None:
        """Set up logging based on configuration."""
        logging.basicConfig(
            level=self.config.get_log_level(),
            format=self.config.get_log_format()
        )

    def _download_all(self) -> None:
        """Download all factsheets and return their paths.

        Returns:
            A dictionary mapping factsheet names to their downloaded file paths.
        """
        results = {}
        downloader = FileDownloader(self.config)
        for factsheet in self.config.get_files_list():
            results[factsheet.name] = downloader.download_file(factsheet)

    def run(self) -> None:
        """Run the factsheet downloader application."""
        try:
            self.logger.info("Starting file downloader")
            # Download all factsheets
            self._download_all()

            self.logger.info("file downloader completed")

        except Exception as e:
            self.logger.error(f"Error in file downloader: {str(e)}")
            raise

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Download factsheets from URLs.')
    parser.add_argument('--config', '-c', 
                        help='Path to config.json file',
                        required=True)
    return parser.parse_args()

def main() -> None:
    """Main entry point for the factsheet downloader."""
    args = parse_args()
    app = FactsheetDownloaderApp(config_file=args.config)
    app.run()


if __name__ == "__main__":
    main()
