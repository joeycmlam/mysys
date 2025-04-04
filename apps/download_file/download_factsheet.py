import requests
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def download_factsheet(url: str, output_dir: str = 'downloads') -> str:
    """
    Download a factsheet PDF from the given URL.
    
    Args:
        url (str): URL of the factsheet PDF
        output_dir (str): Directory to save the downloaded file
        
    Returns:
        str: Path to the downloaded file
    """
    try:
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"jpmf_america_factsheet_{timestamp}.pdf"
        filepath = Path(output_dir) / filename
        
        # Download the file
        logger.info(f"Downloading factsheet from {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Save the file
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        logger.info(f"Factsheet downloaded successfully to {filepath}")
        return str(filepath)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading factsheet: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

def main():
    """Main function to execute the download."""
    url = "https://am.jpmorgan.com/content/dam/jpm-am-aem/asiapacific/hk/en/literature/fact-sheet/jpmf-america_e.pdf"
    
    try:
        filepath = download_factsheet(url)
        logger.info(f"Download completed successfully. File saved at: {filepath}")
    except Exception as e:
        logger.error(f"Failed to download factsheet: {e}")

if __name__ == "__main__":
    main() 