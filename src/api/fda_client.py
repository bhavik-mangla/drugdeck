import json
import requests
import logging
import time
from urllib.parse import quote

class FDAClient:
    """Client for fetching drug information from FDA data sources."""
    
    def __init__(self, local_data_path):
        """Initialize the FDA client with the path to local drug-ndc.json file."""
        self.local_data_path = local_data_path
        self.base_url = "https://api.fda.gov/drug"
        self.logger = logging.getLogger('drugdeck.fda_client')
        self.logger.info("FDA client initialized")
    
    def get_drug_info(self, ndc_code):
        """
        Get drug information based on NDC code from local JSON file.
        
        Args:
            ndc_code (str): NDC code of the drug
            
        Returns:
            dict: Drug information or None if not found
        """
        self.logger.info(f"Searching for drug with NDC: {ndc_code} in local data")
        try:
            start_time = time.time()
            with open(self.local_data_path, 'r') as file:
                self.logger.info(f"Local data file opened: {self.local_data_path}")
                data = json.load(file)
                self.logger.info(f"Local data loaded in {time.time() - start_time:.2f} seconds")
                
            # Search for the drug with the matching NDC in the local data
            for drug in data['results']:
                if drug['product_ndc'] == ndc_code:
                    self.logger.info(f"Drug found with NDC: {ndc_code}")
                    self.logger.debug(f"Found drug details: {drug['brand_name']} ({drug['generic_name']})")
                    return drug
            
            self.logger.warning(f"No drug found with NDC: {ndc_code} in local data")
            return None
        except Exception as e:
            self.logger.error(f"Error loading drug data: {e}")
            return None
    
    def get_drug_label(self, ndc_code):
        """
        Fetch drug label information from FDA API.
        
        Args:
            ndc_code (str): NDC code of the drug
            
        Returns:
            dict: Drug label information
        """
        self.logger.info(f"Fetching drug label for NDC: {ndc_code} from FDA API")
        try:
            url = f"{self.base_url}/label.json?search=openfda.product_ndc:{quote(ndc_code)}&limit=1"
            self.logger.debug(f"FDA API request: {url}")
            
            start_time = time.time()
            response = requests.get(url)
            request_time = time.time() - start_time
            self.logger.info(f"FDA API response received in {request_time:.2f} seconds (status: {response.status_code})")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('results') and len(data['results']) > 0:
                    self.logger.info(f"Drug label found for NDC: {ndc_code}")
                    return data['results'][0]
                else:
                    self.logger.warning(f"No label results found for NDC: {ndc_code}")
            else:
                self.logger.error(f"FDA API error: {response.status_code} - {response.text}")
            
            return None
        except Exception as e:
            self.logger.error(f"Error fetching drug label: {e}")
            return None
    
    def get_drug_approval_info(self, ndc_code):
        """
        Fetch drug approval information from FDA's drugsfda API.
        
        Args:
            ndc_code (str): NDC code of the drug
            
        Returns:
            dict: Drug approval information
        """
        self.logger.info(f"Fetching drug approval info for NDC: {ndc_code} from FDA API")
        try:
            url = f"{self.base_url}/drugsfda.json?search=openfda.product_ndc:{quote(ndc_code)}&limit=1"
            self.logger.debug(f"FDA API request: {url}")
            
            start_time = time.time()
            response = requests.get(url)
            request_time = time.time() - start_time
            self.logger.info(f"FDA API response received in {request_time:.2f} seconds (status: {response.status_code})")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('results') and len(data['results']) > 0:
                    self.logger.info(f"Drug approval info found for NDC: {ndc_code}")
                    return data['results'][0]
                else:
                    self.logger.warning(f"No approval info found for NDC: {ndc_code}")
            else:
                self.logger.error(f"FDA API error: {response.status_code} - {response.text}")
            
            return None
        except Exception as e:
            self.logger.error(f"Error fetching drug approval info: {e}")
            return None
    
    def extract_clinical_trials(self, approval_info):
        """
        Extract clinical trial NCT IDs from approval information.
        
        Args:
            approval_info (dict): Drug approval information
            
        Returns:
            list: List of NCT IDs
        """
        self.logger.info("Attempting to extract clinical trial information")
        # This is a placeholder - in a real implementation, 
        # you would need to parse the medical review document
        # This is complex and might require additional APIs or web scraping
        return []
    
    def get_company_name(self, drug_info, label_info):
        """
        Extract the actual company name from FDA label.
        
        Args:
            drug_info (dict): Basic drug information
            label_info (dict): Drug label information
            
        Returns:
            str: Company name
        """
        self.logger.info("Extracting company name from drug information")
        company_name = drug_info.get('openfda', {}).get('manufacturer_name', [None])[0]
        self.logger.debug(f"Initial company name from drug info: {company_name}")
        
        # Try to extract a more accurate company name from the label
        if label_info and 'adverse_reactions' in label_info:
            self.logger.debug("Attempting to extract company name from adverse reactions text")
            adverse_text = label_info['adverse_reactions'][0]
            if 'SUSPECTED ADVERSE REACTIONS, contact ' in adverse_text:
                parts = adverse_text.split('SUSPECTED ADVERSE REACTIONS, contact ')[1].split(' at ')[0]
                if parts:
                    company_name = parts.strip()
                    self.logger.info(f"Company name extracted from label: {company_name}")
        
        return company_name