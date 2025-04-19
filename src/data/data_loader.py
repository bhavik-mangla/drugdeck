import json
import os

class DataLoader:
    """Utility for loading and managing drug data from local sources."""
    
    def __init__(self, data_path):
        """
        Initialize the data loader with the path to data files.
        
        Args:
            data_path (str): Path to the data directory
        """
        self.data_path = data_path
        
    def load_drug_ndc_data(self):
        """
        Load the drug NDC data from JSON file.
        
        Returns:
            dict: The loaded JSON data
        """
        try:
            with open(os.path.join(self.data_path, 'drug-ndc.json'), 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading drug NDC data: {e}")
            return None
    
    def find_drug_by_ndc(self, ndc_code):
        """
        Find a drug by its NDC code.
        
        Args:
            ndc_code (str): NDC code to search for
            
        Returns:
            dict: Drug information or None if not found
        """
        data = self.load_drug_ndc_data()
        if not data:
            return None
        
        for drug in data.get('results', []):
            if drug.get('product_ndc') == ndc_code:
                return drug
        
        return None
