
import re
import json
import datetime

def format_ndc(ndc_code):
    """
    Format an NDC code to standard format.
    
    Args:
        ndc_code (str): NDC code in any format
        
    Returns:
        str: Formatted NDC code
    """
    # Remove any non-numeric characters
    digits = re.sub(r'\D', '', ndc_code)
    
    # Handle different NDC formats
    if len(digits) == 11:
        # 5-4-2 format
        return f"{digits[:5]}-{digits[5:9]}-{digits[9:]}"
    elif len(digits) == 10:
        # Could be 5-3-2 or 4-4-2
        if ndc_code.startswith('0'):
            return f"{digits[:4]}-{digits[4:8]}-{digits[8:]}"
        else:
            return f"{digits[:5]}-{digits[5:8]}-{digits[8:]}"
    else:
        # Return as is if we can't determine the format
        return ndc_code

def parse_date(date_str):
    """
    Parse date string into a datetime object.
    
    Args:
        date_str (str): Date string in YYYYMMDD format
        
    Returns:
        datetime.date: Parsed date or None if invalid
    """
    if not date_str or len(date_str) != 8:
        return None
    
    try:
        year = int(date_str[:4])
        month = int(date_str[4:6])
        day = int(date_str[6:8])
        return datetime.date(year, month, day)
    except ValueError:
        return None

def format_date(date_str, output_format="%B %d, %Y"):
    """
    Format a date string from YYYYMMDD to a more readable format.
    
    Args:
        date_str (str): Date string in YYYYMMDD format
        output_format (str): Output date format
        
    Returns:
        str: Formatted date string
    """
    parsed_date = parse_date(date_str)
    if parsed_date:
        return parsed_date.strftime(output_format)
    return date_str

def save_json(data, filename):
    """
    Save data to a JSON file.
    
    Args:
        data: Data to save
        filename (str): Filename to save to
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def load_json(filename):
    """
    Load data from a JSON file.
    
    Args:
        filename (str): Filename to load from
        
    Returns:
        dict: Loaded JSON data
    """
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {filename}: {e}")
        return None

def handle_error(error_message):
    print(f"Error: {error_message}")
