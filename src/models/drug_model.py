class Drug:
    """Model representing a drug with all its information."""
    
    def __init__(self, ndc_code, drug_info=None):
        """
        Initialize a Drug object.
        
        Args:
            ndc_code (str): NDC code of the drug
            drug_info (dict, optional): Drug information dictionary
        """
        self.ndc_code = ndc_code
        self.drug_info = drug_info or {}
        
        # Extract basic properties
        self.brand_name = self.drug_info.get('brand_name', 'Unknown')
        self.generic_name = self.drug_info.get('generic_name', 'Unknown')
        self.dosage_form = self.drug_info.get('dosage_form', 'Unknown')
        self.route = self.drug_info.get('route', ['Unknown'])
        self.active_ingredients = self.drug_info.get('active_ingredients', [])
        self.labeler_name = self.drug_info.get('labeler_name', 'Unknown')
        
        # OpenFDA data if available
        openfda = self.drug_info.get('openfda', {})
        self.manufacturer_name = openfda.get('manufacturer_name', ['Unknown'])[0] if openfda.get('manufacturer_name') else 'Unknown'
        self.is_original_packager = openfda.get('is_original_packager', [False])[0] if openfda.get('is_original_packager') else False
        
        # Marketing data
        self.marketing_category = self.drug_info.get('marketing_category', 'Unknown')
        self.marketing_start_date = self.drug_info.get('marketing_start_date', 'Unknown')
        self.application_number = self.drug_info.get('application_number', 'Unknown')
        self.product_type = self.drug_info.get('product_type', 'Unknown')
        self.listing_expiration_date = self.drug_info.get('listing_expiration_date', 'Unknown')
        self.packaging = self.drug_info.get('packaging', [])
    
    def get_active_ingredients_str(self):
        """Get a string representation of active ingredients."""
        if not self.active_ingredients:
            return "Unknown"
        
        ingredients = []
        for ingredient in self.active_ingredients:
            name = ingredient.get('name', 'Unknown')
            strength = ingredient.get('strength', 'Unknown')
            ingredients.append(f"{name} ({strength})")
        
        return ", ".join(ingredients)
    
    def is_otc(self):
        """Check if the drug is over-the-counter."""
        return "OTC" in self.marketing_category
    
    def is_prescription(self):
        """Check if the drug is prescription-only."""
        return "OTC" not in self.marketing_category
    
    def get_application_type(self):
        """Get the application type (NDA, ANDA, BLA)."""
        if not self.application_number:
            return "Unknown"
        
        if self.application_number.startswith("N"):
            return "NDA"
        elif self.application_number.startswith("ANDA"):
            return "ANDA"
        elif self.application_number.startswith("BLA"):
            return "BLA"
        else:
            return "Other"
    
    def __str__(self):
        """String representation of the drug."""
        return f"{self.brand_name} ({self.generic_name}) - NDC: {self.ndc_code}"