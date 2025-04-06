import logging
from pathlib import Path
from typing import Dict, List
from config import Config, FactsheetConfig
from downloader import FactsheetDownloader


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

    def run(self) -> None:
        """Run the factsheet downloader application."""
        try:
            self.logger.info("Starting factsheet downloader")

            # Process each factsheet
            for factsheet in self.config.get_factsheets():
                try:
                    self._process_factsheet(factsheet)
                except Exception as e:
                    self.logger.error(f"Error processing factsheet {factsheet.name}: {str(e)}")
                    continue

            self.logger.info("Factsheet downloader completed")

        except Exception as e:
            self.logger.error(f"Error in factsheet downloader: {str(e)}")
            raise

    def _process_factsheet(self, factsheet: FactsheetConfig) -> None:
        """Process a single factsheet.
        
        Args:
            factsheet: The factsheet configuration to process.
        """
        self.logger.info(f"Processing factsheet: {factsheet.url}")

        # Create downloader instance
        downloader = FactsheetDownloader(self.config)

        # Download factsheet
        downloader.download_factsheet(factsheet)

        self.logger.info(f"Successfully processed factsheet: {factsheet.name}")


def main() -> None:
    """Main entry point for the factsheet downloader."""
    app = FactsheetDownloaderApp()
    app.run()


if __name__ == "__main__":
    main()
