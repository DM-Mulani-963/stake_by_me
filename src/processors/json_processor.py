"""JSON file processor for parsing input data"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class JSONProcessor:
    """Process JSON files containing registration data"""
    
    def __init__(self, input_folder: str = "./data"):
        self.input_folder = Path(input_folder)
        self.required_fields = [
            "email", "username", "password", "dateofbirth", "phonenumber",
            "firstname", "lastname", "country", "place_of_birth",
            "residential_address", "city", "postal_code",
            "occupation_industry", "occupation_field", "occupation_experience"
        ]
        # Note: The test data has different field names from driving licenses
        # We'll map those fields in real implementation
    
    def discover_json_files(self) -> List[Path]:
        """Discover all JSON files in the input folder"""
        if not self.input_folder.exists():
            logger.warning(f"Input folder {self.input_folder} does not exist")
            return []
        
        json_files = list(self.input_folder.glob("*.json"))
        logger.info(f"Found {len(json_files)} JSON files in {self.input_folder}")
        return json_files
    
    def parse_json_file(self, file_path: Path) -> Optional[List[Dict]]:
        """Parse a single JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both single object and array
            if isinstance(data, dict):
                data = [data]
            elif not isinstance(data, list):
                logger.error(f"Invalid JSON format in {file_path}: expected object or array")
                return None
            
            logger.info(f"Successfully parsed {file_path}: {len(data)} records")
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in {file_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return None
    
    def map_license_to_registration(self, license_data: Dict) -> Dict:
        """
        Map driving license data to registration fields
        
        The input JSON has driving license fields, we need to map them
        to the registration form fields
        """
        # Parse date of birth from DD/MM/YYYY to YYYY-MM-DD
        dob = license_data.get("date_of_birth", "")
        if dob and "/" in dob:
            try:
                dob_obj = datetime.strptime(dob, "%d/%m/%Y")
                dob = dob_obj.strftime("%Y-%m-%d")
            except:
                pass
        
        # Split name into first and last
        full_name = license_data.get("name", "")
        name_parts = full_name.split()
        firstname = " ".join(name_parts[:-1]) if len(name_parts) > 1 else full_name
        lastname = name_parts[-1] if len(name_parts) > 1 else ""
        
        # Build address from multiple fields
        address_parts = [
            license_data.get("address", ""),
            license_data.get("address1", ""),
            license_data.get("address2", ""),
        ]
        residential_address = " ".join(filter(None, address_parts)).strip()
        
        # Map to expected format
        mapped_data = {
            # From license data
            "dateofbirth": dob,
            "firstname": firstname,
            "lastname": lastname,
            "country": "India",  # Derived from state
            "state": license_data.get("state", ""),
            "place_of_birth": license_data.get("state", ""),  # Use state as placeholder
            "residential_address": residential_address,
            "city": self._extract_city(license_data.get("address2", "")),
            "postal_code": str(license_data.get("pincode", "")),
            "phonenumber": license_data.get("emergency_contact", ""),
            
            # Additional license info (for reference)
            "full_name": full_name,
            "blood_group": license_data.get("blood_group", ""),
            "license_number": license_data.get("driving_licence_number", ""),
            
            # Fields that need to be generated
            "email": None,
            "username": None,
            "password": None,
            "occupation_industry": None,
            "occupation_field": None,
            "occupation_experience": None,
        }
        
        return mapped_data
    
    def _extract_city(self, address2: str) -> str:
        """Extract city from address2 field (e.g., 'Junagadh, Gujarat' -> 'Junagadh')"""
        if not address2:
            return ""
        parts = address2.split(",")
        return parts[0].strip() if parts else address2.strip()
    
    def validate_record(self, record: Dict) -> tuple[bool, List[str]]:
        """
        Validate a single record
        Returns: (is_valid, list_of_missing_fields)
        """
        missing_fields = []
        
        for field in self.required_fields:
            if field not in record or record[field] is None or record[field] == "":
                missing_fields.append(field)
        
        is_valid = len(missing_fields) == 0
        
        if not is_valid:
            logger.debug(f"Record validation: {len(missing_fields)} missing fields")
        
        return is_valid, missing_fields
    
    def process_all_files(self) -> List[Dict]:
        """
        Process all JSON files in the input folder
        Returns list of all records from all files
        """
        all_records = []
        json_files = self.discover_json_files()
        
        for json_file in json_files:
            records = self.parse_json_file(json_file)
            if records:
                # Map each record from license format to registration format
                mapped_records = [self.map_license_to_registration(r) for r in records]
                
                # Add source file info
                for record in mapped_records:
                    record["_source_file"] = json_file.name
                
                all_records.extend(mapped_records)
        
        logger.info(f"Processed {len(all_records)} total records from {len(json_files)} files")
        return all_records


# Convenience function
def process_json_files(input_folder: str = "./data") -> List[Dict]:
    """Process all JSON files in the input folder"""
    processor = JSONProcessor(input_folder)
    return processor.process_all_files()
