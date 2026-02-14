"""Synthetic data generator for missing fields"""

import random
import string
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
from faker import Faker

logger = logging.getLogger(__name__)

# Initialize Faker
fake = Faker("en_IN")  # Indian English for realistic Indian data


class DataGenerator:
    """Generate synthetic data for missing registration fields"""
    
    def __init__(self):
        self.fake = fake
        
        # Occupation data
        self.industries = [
            "Technology", "Finance", "Healthcare", "Education", "Retail",
            "Manufacturing", "Consulting", "Real Estate", "Transportation",
            "Hospitality", "Construction", "Agriculture"
        ]
        
        self.fields = [
            "Engineering", "Management", "Sales", "Marketing", "Operations",
            "Research", "Customer Service", "Human Resources", "Finance",
            "Administration", "Quality Assurance", "Business Development"
        ]
        
        self.experience_levels = [
            "0-2 years", "3-5 years", "6-10 years", "10+ years"
        ]
        
        # Indian states and cities
        self.states = [
            "Maharashtra", "Gujarat", "Karnataka", "Tamil Nadu", "Delhi",
            "West Bengal", "Rajasthan", "Uttar Pradesh", "Kerala", "Punjab"
        ]
        
        self.cities_by_state = {
            "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar"],
            "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
            "Karnataka": ["Bangalore", "Mysore", "Mangalore", "Hubli"],
            "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem"],
            "Delhi": ["New Delhi", "South Delhi", "North Delhi"],
        }
    
    def generate_email(self, firstname: Optional[str] = None, lastname: Optional[str] = None) -> str:
        """Generate email address"""
        if firstname and lastname:
            # Create email from name
            first = firstname.lower().replace(" ", "")
            last = lastname.lower().replace(" ", "")
            number = random.randint(1, 999)
            
            domains = ["gmail.com", "yahoo.com", "outlook.com", "protonmail.com"]
            domain = random.choice(domains)
            
            patterns = [
                f"{first}.{last}@{domain}",
                f"{first}{last}@{domain}",
                f"{first}.{last}{number}@{domain}",
                f"{first}{number}@{domain}",
            ]
            return random.choice(patterns)
        else:
            return self.fake.email()
    
    def generate_username(self, firstname: Optional[str] = None, lastname: Optional[str] = None) -> str:
        """Generate username"""
        if firstname and lastname:
            first = firstname.lower().replace(" ", "")[:8]
            last = lastname.lower().replace(" ", "")[:8]
            number = random.randint(10, 9999)
            
            patterns = [
                f"{first}_{last}",
                f"{first}{last}",
                f"{first}_{number}",
                f"{first}{last}{number}",
            ]
            return random.choice(patterns)
        else:
            return self.fake.user_name()
    
    def generate_password(self, length: int = 12) -> str:
        """Generate secure password"""
        # Ensure password meets complexity requirements
        uppercase = random.choice(string.ascii_uppercase)
        lowercase = ''.join(random.choices(string.ascii_lowercase, k=5))
        digits = ''.join(random.choices(string.digits, k=3))
        special = random.choice("!@#$%^&*")
        
        # Combine and shuffle
        password_chars = list(uppercase + lowercase + digits + special)
        
        # Add more random chars to reach desired length
        remaining = length - len(password_chars)
        if remaining > 0:
            all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
            password_chars.extend(random.choices(all_chars, k=remaining))
        
        random.shuffle(password_chars)
        return ''.join(password_chars)
    
    def generate_date_of_birth(self, min_age: int = 18, max_age: int = 80) -> str:
        """Generate date of birth (YYYY-MM-DD format)"""
        today = datetime.now()
        start_date = today - timedelta(days=max_age * 365)
        end_date = today - timedelta(days=min_age * 365)
        
        dob = self.fake.date_between(start_date=start_date, end_date=end_date)
        return dob.strftime("%Y-%m-%d")
    
    def generate_phone_number(self, country: str = "India") -> str:
        """Generate phone number"""
        # Indian mobile number format: +91XXXXXXXXXX
        if country in ["India", "IN", "Gujarat", "Maharashtra"]:
            # Start with 6, 7, 8, or 9
            first_digit = random.choice(['6', '7', '8', '9'])
            remaining = ''.join(random.choices(string.digits, k=9))
            return f"91{first_digit}{remaining}"
        else:
            return self.fake.phone_number()
    
    def generate_address(self, city: Optional[str] = None, state: Optional[str] = None) -> str:
        """Generate residential address"""
        if not city or not state:
            state = random.choice(self.states)
            cities = self.cities_by_state.get(state, ["Unknown City"])
            city = random.choice(cities)
        
        house_no = f"H.No. {random.randint(1, 999)}"
        street = self.fake.street_name()
        
        return f"{house_no}, {street}, {city}, {state}"
    
    def generate_postal_code(self, state: Optional[str] = None) -> str:
        """Generate postal code (PIN code for India)"""
        # Indian PIN codes are 6 digits
        # First digit typically represents region
        region_map = {
            "Gujarat": "3",
            "Maharashtra": "4",
            "Karnataka": "5",
            "Tamil Nadu": "6",
            "Delhi": "1",
        }
        
        first_digit = region_map.get(state, random.choice(list(region_map.values())))
        remaining = ''.join(random.choices(string.digits, k=5))
        
        return f"{first_digit}{remaining}"
    
    def generate_occupation_industry(self) -> str:
        """Generate occupation industry"""
        return random.choice(self.industries)
    
    def generate_occupation_field(self) -> str:
        """Generate occupation field"""
        return random.choice(self.fields)
    
    def generate_occupation_experience(self) -> str:
        """Generate occupation experience"""
        return random.choice(self.experience_levels)
    
    def generate_city(self, state: Optional[str] = None) -> str:
        """Generate city name"""
        if state and state in self.cities_by_state:
            return random.choice(self.cities_by_state[state])
        return self.fake.city()
    
    def generate_place_of_birth(self, state: Optional[str] = None) -> str:
        """Generate place of birth"""
        return self.generate_city(state) if state else self.fake.city()
    
    def fill_missing_fields(self, record: Dict) -> Dict:
        """
        Fill in missing fields with generated data
        Maintains consistency (e.g., state-city-postal code)
        """
        filled = record.copy()
        
        # Get existing values for consistency
        state = filled.get("state") or filled.get("country") or "Gujarat"
        city = filled.get("city")
        firstname = filled.get("firstname")
        lastname = filled.get("lastname")
        
        # Generate missing fields
        if not filled.get("email"):
            filled["email"] = self.generate_email(firstname, lastname)
        
        if not filled.get("username"):
            filled["username"] = self.generate_username(firstname, lastname)
        
        if not filled.get("password"):
            filled["password"] = self.generate_password()
        
        if not filled.get("dateofbirth"):
            filled["dateofbirth"] = self.generate_date_of_birth()
        
        if not filled.get("phonenumber"):
            filled["phonenumber"] = self.generate_phone_number()
        
        if not filled.get("firstname"):
            filled["firstname"] = self.fake.first_name()
        
        if not filled.get("lastname"):
            filled["lastname"] = self.fake.last_name()
        
        if not filled.get("country"):
            filled["country"] = "India"
        
        if not filled.get("place_of_birth"):
            filled["place_of_birth"] = self.generate_place_of_birth(state)
        
        if not filled.get("residential_address"):
            filled["residential_address"] = self.generate_address(city, state)
        
        if not filled.get("city"):
            filled["city"] = self.generate_city(state)
        
        if not filled.get("postal_code"):
            filled["postal_code"] = self.generate_postal_code(state)
        
        if not filled.get("occupation_industry"):
            filled["occupation_industry"] = self.generate_occupation_industry()
        
        if not filled.get("occupation_field"):
            filled["occupation_field"] = self.generate_occupation_field()
        
        if not filled.get("occupation_experience"):
            filled["occupation_experience"] = self.generate_occupation_experience()
        
        return filled


# Convenience function
def fill_missing_data(records: list[Dict]) -> list[Dict]:
    """Fill missing data in multiple records"""
    generator = DataGenerator()
    return [generator.fill_missing_fields(record) for record in records]
