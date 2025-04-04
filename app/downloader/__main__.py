from config import Config
from downloader import FactsheetDownloader

def main():
    """Main entry point for the factsheet downloader."""
    try:
        # Load configuration
        config = Config()
        
        # Initialize downloader
        downloader = FactsheetDownloader(config)
        
        # Download all factsheets
        results = downloader.download_all_factsheets()
        
        # Log results
        for name, filename in results.items():
            if filename:
                print(f"Successfully downloaded factsheet '{name}' to {filename}")
            else:
                print(f"Failed to download factsheet '{name}'")
                
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 