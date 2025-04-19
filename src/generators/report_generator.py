import json
from datetime import datetime

class ReportGenerator:
    """Generator for creating comprehensive drug reports."""
    
    def __init__(self, drug_info, ai_insights, label_info=None):
        """
        Initialize the report generator.
        
        Args:
            drug_info (dict): Basic drug information
            ai_insights (dict): AI-generated insights about the drug
            label_info (dict, optional): FDA label information
        """
        self.drug_info = drug_info
        self.ai_insights = ai_insights
        self.label_info = label_info or {}
        
    def compile_report(self, ndc_code):
        """
        Compile a comprehensive drug report.
        
        Args:
            ndc_code (str): NDC code of the drug
            
        Returns:
            dict: Complete drug report
        """
        report = {
            "meta": {
                "report_id": f"drug_{ndc_code}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "ndc_code": ndc_code,
                "generated_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "report_type": "Drug Deck"
            },
            "drug_information": self._compile_drug_information(),
            "manufacturer_information": self._compile_manufacturer_information(),
            "clinical_information": self._compile_clinical_information(),
            "market_information": self._compile_market_information(),
            "ai_insights": self.ai_insights
        }
        
        # Add label information if available
        if self.label_info:
            report["label_information"] = self.label_info
        
        return report
    
    def _compile_drug_information(self):
        """Compile basic drug information section."""
        drug_info = {
            "brand_name": self.drug_info.get("brand_name", "Unknown"),
            "generic_name": self.drug_info.get("generic_name", "Unknown"),
            "dosage_form": self.drug_info.get("dosage_form", "Unknown"),
            "route": self.drug_info.get("route", ["Unknown"]),
            "active_ingredients": [],
            "marketing_start_date": self.drug_info.get("marketing_start_date", "Unknown"),
            "marketing_category": self.drug_info.get("marketing_category", "Unknown"),
            "application_number": self.drug_info.get("application_number", "Unknown"),
        }
        
        # Process active ingredients
        for ingredient in self.drug_info.get("active_ingredients", []):
            drug_info["active_ingredients"].append({
                "name": ingredient.get("name", "Unknown"),
                "strength": ingredient.get("strength", "Unknown")
            })
        
        return drug_info
    
    def _compile_manufacturer_information(self):
        """Compile manufacturer information section."""
        openfda = self.drug_info.get("openfda", {})
        
        manufacturer_info = {
            "labeler_name": self.drug_info.get("labeler_name", "Unknown"),
            "manufacturer_name": openfda.get("manufacturer_name", ["Unknown"])[0] if openfda.get("manufacturer_name") else "Unknown",
            "is_original_packager": openfda.get("is_original_packager", [False])[0] if openfda.get("is_original_packager") else False,
        }
        
        return manufacturer_info
    
    def _compile_clinical_information(self):
        """Compile clinical information section."""
        clinical_info = {
            "indications": self._get_label_section("indications_and_usage"),
            "contraindications": self._get_label_section("contraindications"),
            "warnings": self._get_label_section("warnings"),
            "adverse_reactions": self._get_label_section("adverse_reactions"),
            "drug_interactions": self._get_label_section("drug_interactions"),
        }
        
        return clinical_info
    
    def _get_label_section(self, section_name):
        """
        Get a specific section from the FDA label.
        
        Args:
            section_name (str): Section name in the label
            
        Returns:
            str: Section text or default message
        """
        if not self.label_info:
            return "Information not available in the basic data. See AI Insights section."
        
        section_data = self.label_info.get(section_name)
        if not section_data:
            return "Information not available in the FDA label. See AI Insights section."
        
        if isinstance(section_data, list) and len(section_data) > 0:
            return section_data[0]
        
        return str(section_data)
    
    def _compile_market_information(self):
        """Compile market information section."""
        market_info = {
            "product_type": self.drug_info.get("product_type", "Unknown"),
            "marketing_status": "Active" if self.drug_info.get("finished", False) else "Unknown",
            "listing_expiration_date": self.drug_info.get("listing_expiration_date", "Unknown"),
            "packaging": []
        }
        
        # Process packaging information
        for package in self.drug_info.get("packaging", []):
            market_info["packaging"].append({
                "package_ndc": package.get("package_ndc", "Unknown"),
                "description": package.get("description", "Unknown"),
                "marketing_start_date": package.get("marketing_start_date", "Unknown"),
                "sample": package.get("sample", False)
            })
        
        return market_info