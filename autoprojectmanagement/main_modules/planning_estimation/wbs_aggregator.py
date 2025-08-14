#!/usr/bin/env python3
"""
WBS Aggregator Module

This module provides functionality to aggregate Work Breakdown Structure (WBS) parts
from multiple JSON files into a single comprehensive WBS structure.

Author: AutoProjectManagement Team
Version: 2.0.0
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
DEFAULT_PARTS_DIR = 'SystemInputs/user_inputs/wbs_parts'
DEFAULT_OUTPUT_FILE = 'SystemInputs/user_inputs/detailed_wbs.json'
SUPPORTED_FILE_EXTENSIONS = ['.json']
ENCODING = 'utf-8'


class WBSAggregatorError(Exception):
    """Custom exception for WBS aggregation errors."""
    pass


class WBSAggregator:
    """
    Aggregates Work Breakdown Structure (WBS) parts from multiple JSON files.
    
    This class provides methods to load individual WBS parts from a directory
    and combine them into a single comprehensive WBS structure.
    
    Attributes:
        parts_dir (str): Directory containing WBS part files
        output_file (str): Path to save the aggregated WBS
    """
    
    def __init__(self, 
                 parts_dir: str = DEFAULT_PARTS_DIR,
                 output_file: str = DEFAULT_OUTPUT_FILE) -> None:
        """
        Initialize the WBS Aggregator.
        
        Args:
            parts_dir: Directory containing WBS part files (default: 'SystemInputs/user_inputs/wbs_parts')
            output_file: Path to save the aggregated WBS (default: 'SystemInputs/user_inputs/detailed_wbs.json')
        
        Raises:
            WBSAggregatorError: If parts_dir or output_file paths are invalid
        """
        self.parts_dir = Path(parts_dir)
        self.output_file = Path(output_file)
        
        # Validate paths
        self._validate_paths()
        
        logger.info(f"Initialized WBSAggregator with parts_dir: {self.parts_dir}")
        logger.info(f"Output file: {self.output_file}")
    
    def _validate_paths(self) -> None:
        """Validate that the parts directory exists and output directory is writable."""
        if not self.parts_dir.exists():
            raise WBSAggregatorError(f"Parts directory does not exist: {self.parts_dir}")
        
        if not self.parts_dir.is_dir():
            raise WBSAggregatorError(f"Parts directory is not a directory: {self.parts_dir}")
        
        # Ensure output directory exists
        output_dir = self.output_file.parent
        output_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_supported_files(self) -> List[Path]:
        """
        Get list of supported WBS part files from the parts directory.
        
        Returns:
            List of Path objects for supported files
        """
        if not self.parts_dir.exists():
            return []
        
        files = []
        for extension in SUPPORTED_FILE_EXTENSIONS:
            files.extend(self.parts_dir.glob(f'*{extension}'))
        
        return sorted(files)  # Sort for consistent ordering
    
    def load_part(self, file_path: Path) -> Dict[str, Any]:
        """
        Load a single WBS part from a JSON file.
        
        Args:
            file_path: Path to the JSON file containing WBS part
            
        Returns:
            Dictionary containing the WBS part data
            
        Raises:
            WBSAggregatorError: If file cannot be loaded or parsed
        """
        try:
            with open(file_path, 'r', encoding=ENCODING) as f:
                data = json.load(f)
                logger.debug(f"Successfully loaded WBS part from: {file_path}")
                return data
        except FileNotFoundError:
            raise WBSAggregatorError(f"File not found: {file_path}")
        except json.JSONDecodeError as e:
            raise WBSAggregatorError(f"Invalid JSON in file {file_path}: {e}")
        except Exception as e:
            raise WBSAggregatorError(f"Error loading file {file_path}: {e}")
    
    def _validate_wbs_part(self, part: Dict[str, Any], file_path: Path) -> bool:
        """
        Validate that a WBS part has the required structure.
        
        Args:
            part: Dictionary containing WBS part data
            file_path: Path to the source file (for error messages)
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ['id', 'name', 'level']
        
        for field in required_fields:
            if field not in part:
                logger.warning(f"Missing required field '{field}' in {file_path}")
                return False
        
        if not isinstance(part.get('level'), int) or part.get('level') < 0:
            logger.warning(f"Invalid level value in {file_path}")
            return False
        
        return True
    
    def aggregate(self) -> Dict[str, Any]:
        """
        Aggregate all WBS parts into a single comprehensive WBS structure.
        
        This method loads all WBS parts from the parts directory, validates them,
        and combines them into a single hierarchical structure.
        
        Returns:
            Dictionary containing the aggregated WBS structure
            
        Raises:
            WBSAggregatorError: If aggregation fails
        """
        logger.info("Starting WBS aggregation process...")
        
        # Get list of supported files
        part_files = self._get_supported_files()
        
        if not part_files:
            logger.warning("No WBS parts found in directory")
            return {}
        
        logger.info(f"Found {len(part_files)} WBS part files to process")
        
        # Initialize root structure
        root = None
        processed_files = 0
        
        for file_path in part_files:
            try:
                part = self.load_part(file_path)
                
                # Validate part structure
                if not self._validate_wbs_part(part, file_path):
                    logger.warning(f"Skipping invalid WBS part: {file_path}")
                    continue
                
                if root is None:
                    # Create root from first valid part
                    root = {
                        "id": part["id"],
                        "name": part["name"],
                        "level": part["level"],
                        "subtasks": []
                    }
                
                # Merge subtasks from this part
                if "subtasks" in part and part["subtasks"]:
                    root["subtasks"].extend(part["subtasks"])
                    processed_files += 1
                    logger.debug(f"Merged subtasks from: {file_path}")
                    
            except WBSAggregatorError as e:
                logger.error(f"Error processing {file_path}: {e}")
                continue
        
        if root is None:
            raise WBSAggregatorError("No valid WBS parts found to aggregate")
        
        logger.info(f"Successfully aggregated {processed_files} WBS parts")
        return root
    
    def save_aggregated_wbs(self, wbs_data: Dict[str, Any]) -> None:
        """
        Save the aggregated WBS data to the output file.
        
        Args:
            wbs_data: Dictionary containing the aggregated WBS structure
            
        Raises:
            WBSAggregatorError: If saving fails
        """
        try:
            with open(self.output_file, 'w', encoding=ENCODING) as f:
                json.dump(wbs_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Aggregated WBS successfully saved to: {self.output_file}")
        except Exception as e:
            raise WBSAggregatorError(f"Error saving aggregated WBS: {e}")
    
    def run(self) -> bool:
        """
        Execute the complete WBS aggregation process.
        
        This is a convenience method that combines aggregation and saving.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            aggregated_wbs = self.aggregate()
            if aggregated_wbs:
                self.save_aggregated_wbs(aggregated_wbs)
                return True
            return False
        except WBSAggregatorError as e:
            logger.error(f"Aggregation failed: {e}")
            return False
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the aggregation process.
        
        Returns:
            Dictionary containing summary information
        """
        part_files = self._get_supported_files()
        
        return {
            "parts_directory": str(self.parts_dir),
            "output_file": str(self.output_file),
            "total_parts_found": len(part_files),
            "supported_extensions": SUPPORTED_FILE_EXTENSIONS,
            "parts_files": [str(f) for f in part_files]
        }


def main() -> None:
    """Main entry point for the WBS aggregator script."""
    try:
        aggregator = WBSAggregator()
        success = aggregator.run()
        
        if success:
            print("✅ WBS aggregation completed successfully")
            summary = aggregator.get_summary()
            print(f"📊 Summary: {summary}")
        else:
            print("❌ WBS aggregation failed")
            exit(1)
            
    except WBSAggregatorError as e:
        logger.error(f"Fatal error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
