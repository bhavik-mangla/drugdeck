import google.generativeai as genai
import json

class GeminiClient:
    """Client for interacting with Google's Gemini API for AI-generated insights."""
    
    def __init__(self, api_key):
        """Initialize the Gemini client with API key."""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def get_ai_insights(self, drug_info):
        """
        Generate AI insights about the drug using Gemini.
        
        Args:
            drug_info (dict): Drug information
            
        Returns:
            dict: AI-generated insights
        """
        insights = {}
        
        # Basic drug summary
        drug_summary = self._generate_drug_summary(drug_info)
        insights['drug_summary'] = drug_summary
        
        # Mechanism of action
        moa = self._generate_mechanism_of_action(drug_info)
        insights['mechanism_of_action'] = moa
        
        # Side effects analysis
        side_effects = self._generate_side_effects_analysis(drug_info)
        insights['side_effects'] = side_effects
        
        # Market trends
        market_trends = self._generate_market_trends(drug_info)
        insights['market_trends'] = market_trends
        
        # Patient journey summary
        patient_journey = self._generate_patient_journey(drug_info)
        insights['patient_journey'] = patient_journey
        
        return insights
    
    def _generate_drug_summary(self, drug_info):
        """Generate a concise summary of the drug."""
        brand_name = drug_info.get('brand_name', 'Unknown Drug')
        generic_name = drug_info.get('generic_name', 'Unknown')
        
        active_ingredients = []
        for ingredient in drug_info.get('active_ingredients', []):
            active_ingredients.append(f"{ingredient.get('name', 'Unknown')}: {ingredient.get('strength', 'Unknown')}")
        
        ingredients_str = ", ".join(active_ingredients) if active_ingredients else "Unknown"
        
        prompt = f"""
        Generate a concise and informative summary for {brand_name} ({generic_name}).
        
        Drug information:
        - Brand name: {brand_name}
        - Generic name: {generic_name}
        - Active ingredients: {ingredients_str}
        - Dosage form: {drug_info.get('dosage_form', 'Unknown')}
        - Route: {', '.join(drug_info.get('route', ['Unknown']))}
        - Manufacturer: {drug_info.get('labeler_name', 'Unknown')}
        
        Provide information about what this drug is used for, its key benefits, and any notable characteristics.
        Limit the response to 3-4 paragraphs.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def _generate_mechanism_of_action(self, drug_info):
        """Generate information about the drug's mechanism of action."""
        brand_name = drug_info.get('brand_name', 'Unknown Drug')
        generic_name = drug_info.get('generic_name', 'Unknown')
        
        active_ingredients = []
        for ingredient in drug_info.get('active_ingredients', []):
            active_ingredients.append(ingredient.get('name', 'Unknown'))
        
        ingredients_str = ", ".join(active_ingredients) if active_ingredients else "Unknown"
        
        prompt = f"""
        Explain the mechanism of action for {brand_name} ({generic_name}) containing {ingredients_str}.
        
        Include:
        1. How the drug works at the molecular level
        2. The physiological processes it affects
        3. How these mechanisms produce therapeutic effects
        
        Make the explanation detailed but accessible, suitable for healthcare professionals.
        Include relevant receptor interactions, pathway modifications, or other cellular/molecular details.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def _generate_side_effects_analysis(self, drug_info):
        """Generate analysis of potential side effects."""
        brand_name = drug_info.get('brand_name', 'Unknown Drug')
        generic_name = drug_info.get('generic_name', 'Unknown')
        
        active_ingredients = []
        for ingredient in drug_info.get('active_ingredients', []):
            active_ingredients.append(ingredient.get('name', 'Unknown'))
        
        ingredients_str = ", ".join(active_ingredients) if active_ingredients else "Unknown"
        
        prompt = f"""
        Provide a comprehensive analysis of the potential side effects for {brand_name} ({generic_name}) containing {ingredients_str}.
        
        Include:
        1. Common side effects and their approximate frequency
        2. Serious but rare side effects that require medical attention
        3. Risk factors that may increase the likelihood of side effects
        4. Any monitoring recommendations for patients using this medication
        
        Organize the information in a structured format suitable for healthcare professionals.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def _generate_market_trends(self, drug_info):
        """Generate market trends analysis for the drug."""
        brand_name = drug_info.get('brand_name', 'Unknown Drug')
        generic_name = drug_info.get('generic_name', 'Unknown')
        
        prompt = f"""
        Analyze the current market trends for {brand_name} ({generic_name}).
        
        Include:
        1. Current market position and competitive landscape
        2. Recent developments or changes in prescribing patterns
        3. Future outlook considering patent status, competing therapies, and emerging alternatives
        4. Any notable regulatory or reimbursement factors affecting this drug
        
        Provide factual, balanced information suitable for business analysis.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def _generate_patient_journey(self, drug_info):
        """Generate patient journey information."""
        brand_name = drug_info.get('brand_name', 'Unknown Drug')
        generic_name = drug_info.get('generic_name', 'Unknown')
        
        prompt = f"""
        Outline a typical patient journey for individuals prescribed {brand_name} ({generic_name}).
        
        Include:
        1. The typical diagnostic process leading to prescription
        2. Initial onboarding experience (first prescription, education, etc.)
        3. Ongoing treatment experience (administration, monitoring, follow-up)
        4. Common challenges patients face and how they're typically addressed
        
        Structure this information to give insight into the patient experience from diagnosis through ongoing treatment.
        """
        
        response = self.model.generate_content(prompt)
        return response.text