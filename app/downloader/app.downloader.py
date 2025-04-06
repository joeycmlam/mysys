import logging
from pathlib import Path
from typing import Dict, List
from config import Config, DownloadConfig
from downloader import FileDownloader


class FactsheetDownloaderApp:
    """Main application class for downloading factsheets."""

    def __init__(self, config_path: str = None):
        """Initialize the factsheet downloader application.
        
        Args:
            config_path: Optional path to config file. If not provided, looks for config.json
                        in the same directory as the calling module.
        """
        self.config = Config(config_path)
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
        for factsheet in self.config.get_factsheets():
            results[factsheet.name] = downloader.download_file(factsheet)



    def run(self) -> None:
        """Run the factsheet downloader application."""
        try:
            self.logger.info("Starting factsheet downloader")
            # Download all factsheets
            self._download_all()

            self.logger.info("Factsheet downloader completed")

        except Exception as e:
            self.logger.error(f"Error in factsheet downloader: {str(e)}")
            raise


def main() -> None:
    """Main entry point for the factsheet downloader."""
    app = FactsheetDownloaderApp()
    app.run()


if __name__ == "__main__":
    main()
