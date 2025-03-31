import os
import yaml
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataExtractor:
    def __init__(self, config_path: str):
        """Initialize the DataExtractor with configuration file path."""
        self.config = self._load_config(config_path)
        self.engine = self._create_engine()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            raise

    def _create_engine(self):
        """Create SQLAlchemy engine based on database configuration."""
        db_config = self.config['database']
        connection_string = f"{db_config['type']}://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        return create_engine(connection_string)

    def _ensure_output_directory(self, file_path: str):
        """Ensure the output directory exists."""
        output_dir = os.path.dirname(file_path)
        if output_dir:
            Path(output_dir).mkdir(parents=True, exist_ok=True)

    def _write_output(self, df: pd.DataFrame, output_config: Dict[str, Any]):
        """Write DataFrame to output file based on configuration."""
        file_path = output_config['file']
        self._ensure_output_directory(file_path)

        if output_config['format'].lower() == 'csv':
            df.to_csv(
                file_path,
                index=False,
                encoding=output_config.get('encoding', 'utf-8')
            )
        elif output_config['format'].lower() == 'excel':
            df.to_excel(
                file_path,
                sheet_name=output_config.get('sheet_name', 'Sheet1'),
                index=False
            )
        else:
            raise ValueError(f"Unsupported output format: {output_config['format']}")

    def execute_query(self, query_name: str):
        """Execute a specific query defined in the configuration."""
        query_config = next(
            (q for q in self.config['queries'] if q['name'] == query_name),
            None
        )
        
        if not query_config:
            raise ValueError(f"Query '{query_name}' not found in configuration")

        try:
            # Execute query with parameters
            with self.engine.connect() as connection:
                result = connection.execute(
                    text(query_config['sql']),
                    query_config.get('parameters', {})
                )
                df = pd.DataFrame(result.fetchall(), columns=result.keys())

            # Write output
            self._write_output(df, query_config['output'])
            logger.info(f"Successfully executed query '{query_name}' and wrote output to {query_config['output']['file']}")
            
        except Exception as e:
            logger.error(f"Error executing query '{query_name}': {e}")
            raise

    def execute_all_queries(self):
        """Execute all queries defined in the configuration."""
        for query in self.config['queries']:
            self.execute_query(query['name'])

def main():
    """Main function to run the data extraction process."""
    try:
        extractor = DataExtractor('config.yaml')
        extractor.execute_all_queries()
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise

if __name__ == "__main__":
    main() 