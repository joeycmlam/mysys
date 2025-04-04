from downloader import FactsheetDownloader

def main():
    """Main entry point for the factsheet downloader."""
    try:
        # Create and run the downloader
        downloader = FactsheetDownloader()
        result = downloader.download()
        
        if result:
            print(f"Factsheet downloaded successfully to: {result}")
        else:
            print("Failed to download factsheet")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 