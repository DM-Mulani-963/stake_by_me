"""Complete data processing pipeline"""

import logging
from pathlib import Path
from typing import List, Dict, Optional

from src.processors.json_processor import JSONProcessor
from src.processors.data_generator import DataGenerator
from src.processors.excel_generator import ExcelGenerator

logger = logging.getLogger(__name__)


class DataPipeline:
    """End-to-end data processing pipeline"""
    
    def __init__(
        self,
        input_folder: str = "./data",
        output_folder: str = "./output"
    ):
        self.json_processor = JSONProcessor(input_folder)
        self.data_generator = DataGenerator()
        self.excel_generator = ExcelGenerator(output_folder)
    
    def process(self, output_filename: Optional[str] = None) -> tuple[Path, List[Dict]]:
        """
        Run complete pipeline:
        1. Parse JSON files
        2. Fill missing data
        3. Generate Excel
        
        Returns:
            (excel_filepath, processed_records)
        """
        logger.info("=" * 60)
        logger.info("Starting data processing pipeline")
        logger.info("=" * 60)
        
        # Step 1: Parse JSON files
        logger.info("Step 1: Parsing JSON files...")
        records = self.json_processor.process_all_files()
        logger.info(f"✓ Parsed {len(records)} records")
        
        if not records:
            logger.error("No records found to process")
            return None, []
        
        # Step 2: Fill missing data
        logger.info("Step 2: Filling missing data...")
        filled_records = []
        for idx, record in enumerate(records, 1):
            logger.debug(f"Processing record {idx}/{len(records)}")
            filled = self.data_generator.fill_missing_fields(record)
            filled_records.append(filled)
        logger.info(f"✓ Filled missing data for {len(filled_records)} records")
        
        # Step 3: Generate Excel
        logger.info("Step 3: Generating Excel file...")
        excel_path = self.excel_generator.create_excel(filled_records, output_filename)
        logger.info(f"✓ Excel file created: {excel_path}")
        
        logger.info("=" * 60)
        logger.info("Pipeline completed successfully!")
        logger.info("=" * 60)
        
        return excel_path, filled_records


def run_pipeline(
    input_folder: str = "./data",
    output_folder: str = "./output",
    output_filename: Optional[str] = None
) -> tuple[Path, List[Dict]]:
    """Convenience function to run the complete pipeline"""
    pipeline = DataPipeline(input_folder, output_folder)
    return pipeline.process(output_filename)


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Run pipeline
    excel_file, records = run_pipeline()
    
    if excel_file:
        print(f"\n✓ Success! Excel file created at: {excel_file}")
        print(f"✓ Total records processed: {len(records)}")
    else:
        print("\n✗ Pipeline failed")
