from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
import json
import os
import logging
import time
from datetime import datetime

class PDFGenerator:
    """Generator for creating PDF reports from drug information."""
    
    def __init__(self, report_data, output_file):
        """
        Initialize the PDF generator.
        
        Args:
            report_data (dict): Compiled report data
            output_file (str): Path to the output PDF file
        """
        self.report_data = report_data
        self.output_file = output_file
        self.styles = getSampleStyleSheet()
        self.logger = logging.getLogger('drugdeck.pdf_generator')
        self.logger.info("PDF Generator initialized")
        self._define_styles()
        
    def _define_styles(self):
        """Define custom styles for the PDF."""
        self.logger.debug("Defining custom PDF styles")
        self.styles.add(ParagraphStyle(
            name='DrugDeckTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=12,
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='DrugDeckHeading2',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=6,
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='DrugDeckHeading3',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=6,
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='DrugDeckNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6
        ))
        
        self.styles.add(ParagraphStyle(
            name='DrugDeckFooter',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.grey
        ))
        
        self.styles.add(ParagraphStyle(
            name='DrugDeckBullet',
            parent=self.styles['Normal'],
            fontSize=11,
            leftIndent=20,
            bulletIndent=10,
            spaceAfter=3
        ))
    
    def generate_pdf(self):
        """Generate the PDF report."""
        self.logger.info(f"Generating PDF report: {self.output_file}")
        start_time = time.time()
        
        # Create PDF document with custom footer
        doc = SimpleDocTemplate(
            self.output_file, 
            pagesize=letter,
            rightMargin=0.5*inch, 
            leftMargin=0.5*inch,
            topMargin=0.5*inch, 
            bottomMargin=0.75*inch  # Increased to accommodate footer
        )
        
        # Define a footer function to add timestamps
        def add_footer(canvas, doc):
            canvas.saveState()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            footer_text = f"Generated on: {timestamp} | DrugDeck Report"
            canvas.setFont('Helvetica', 8)
            canvas.setFillColor(colors.grey)
            canvas.drawString(0.5*inch, 0.5*inch, footer_text)
            canvas.restoreState()
        
        story = []
        
        # Add title
        drug_info = self.report_data.get("drug_information", {})
        title = f"Drug Deck: {drug_info.get('brand_name', 'Unknown Drug')}"
        story.append(Paragraph(title, self.styles["DrugDeckTitle"]))
        story.append(Spacer(1, 0.25*inch))
        
        # Add metadata
        meta = self.report_data.get("meta", {})
        meta_text = f"NDC Code: {meta.get('ndc_code', 'Unknown')}<br/>"
        meta_text += f"Report Generated: {meta.get('generated_date', 'Unknown')}"
        story.append(Paragraph(meta_text, self.styles["DrugDeckNormal"]))
        story.append(Spacer(1, 0.25*inch))
        
        # Add drug information section
        story.append(Paragraph("Drug Information", self.styles["DrugDeckHeading2"]))
        for item in self._create_drug_info_table():
            story.append(item)
        story.append(Spacer(1, 0.25*inch))
        
        # Add manufacturer information section
        story.append(Paragraph("Manufacturer Information", self.styles["DrugDeckHeading2"]))
        story.append(self._create_manufacturer_info_table())
        story.append(Spacer(1, 0.25*inch))
        
        # Add FDA Label section if available
        label_info = self.report_data.get("label_information", {})
        if label_info:
            self.logger.info("Adding FDA label information to PDF")
            story.append(Paragraph("FDA Label Information", self.styles["DrugDeckHeading2"]))
            for item in self._create_label_info_section():
                story.append(item)
            story.append(Spacer(1, 0.25*inch))
        else:
            self.logger.info("No FDA label information available")
        
        # Add clinical information section
        story.append(Paragraph("Clinical Information", self.styles["DrugDeckHeading2"]))
        for item in self._create_clinical_info_section():
            story.append(item)
        story.append(Spacer(1, 0.25*inch))
        
        # Add market information section
        story.append(Paragraph("Market Information", self.styles["DrugDeckHeading2"]))
        for item in self._create_market_info_section():
            story.append(item)
        story.append(Spacer(1, 0.25*inch))
        
        # Add AI insights
        story.append(Paragraph("AI-Generated Insights", self.styles["DrugDeckHeading2"]))
        for item in self._create_ai_insights_section():
            story.append(item)
        
        # Build the PDF with custom footer
        self.logger.debug("Building PDF document")
        doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
        
        self.logger.info(f"PDF report generated in {time.time() - start_time:.2f} seconds: {self.output_file}")

    # All other methods remain the same
    def _create_drug_info_table(self):
        """Create a table with drug information."""
        drug_info = self.report_data.get("drug_information", {})
        
        # Prepare data for the table
        data = [
            ["Brand Name", drug_info.get("brand_name", "Unknown")],
            ["Generic Name", drug_info.get("generic_name", "Unknown")],
            ["Dosage Form", drug_info.get("dosage_form", "Unknown")],
            ["Route", ", ".join(drug_info.get("route", ["Unknown"]))],
            ["Marketing Start Date", drug_info.get("marketing_start_date", "Unknown")],
            ["Marketing Category", drug_info.get("marketing_category", "Unknown")],
            ["Application Number", drug_info.get("application_number", "Unknown")]
        ]
        
        # Create the table
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.darkblue),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        result = [table]
        
        # Add active ingredients
        ingredients = drug_info.get("active_ingredients", [])
        if ingredients:
            ingredients_text = "Active Ingredients:<br/>"
            for ingredient in ingredients:
                ingredients_text += f"• {ingredient.get('name', 'Unknown')}: {ingredient.get('strength', 'Unknown')}<br/>"
            
            result.append(Spacer(1, 0.1*inch))
            result.append(Paragraph(ingredients_text, self.styles["DrugDeckNormal"]))  # Updated style name
        
        return result
    
    def _create_manufacturer_info_table(self):
        """Create a table with manufacturer information."""
        manufacturer_info = self.report_data.get("manufacturer_information", {})
        
        # Prepare data for the table
        data = [
            ["Labeler Name", manufacturer_info.get("labeler_name", "Unknown")],
            ["Manufacturer Name", manufacturer_info.get("manufacturer_name", "Unknown")],
            ["Original Packager", "Yes" if manufacturer_info.get("is_original_packager", False) else "No"]
        ]
        
        # Create the table
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.darkblue),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        return table
    
    def _create_label_info_section(self):
        """Create the FDA label information section."""
        label_info = self.report_data.get("label_information", {})
        
        result = []
        
        # Skip these sections as they might be covered elsewhere
        skip_sections = ["openfda", "spl_product_data_elements", "spl_id", "id", "set_id"]
        
        for key, value in label_info.items():
            if key in skip_sections:
                continue
                
            if value:
                heading = key.replace("_", " ").title()
                result.append(Paragraph(heading, self.styles["DrugDeckHeading3"]))  # Updated style name
                
                # Handle list or string values
                if isinstance(value, list):
                    if len(value) > 0:
                        # Join multiple items with line breaks
                        text = "<br/>".join(str(item) for item in value)
                        result.append(Paragraph(text, self.styles["DrugDeckNormal"]))  # Updated style name
                else:
                    result.append(Paragraph(str(value), self.styles["DrugDeckNormal"]))  # Updated style name
                    
                result.append(Spacer(1, 0.1*inch))
        
        return result
    
    def _create_clinical_info_section(self):
        """Create the clinical information section."""
        clinical_info = self.report_data.get("clinical_information", {})
        
        result = []
        
        for key, value in clinical_info.items():
            heading = key.replace("_", " ").title()
            result.append(Paragraph(heading, self.styles["DrugDeckHeading3"]))  # Updated style name
            result.append(Paragraph(value, self.styles["DrugDeckNormal"]))  # Updated style name
            result.append(Spacer(1, 0.1*inch))
        
        return result
    
    def _create_market_info_section(self):
        """Create the market information section."""
        market_info = self.report_data.get("market_information", {})
        
        # Prepare data for the table
        data = [
            ["Product Type", market_info.get("product_type", "Unknown")],
            ["Marketing Status", market_info.get("marketing_status", "Unknown")],
            ["Listing Expiration Date", market_info.get("listing_expiration_date", "Unknown")]
        ]
        
        # Create the table
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.darkblue),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        result = [table]
        
        # Add packaging information
        packaging = market_info.get("packaging", [])
        if packaging:
            result.append(Spacer(1, 0.1*inch))
            result.append(Paragraph("Packaging Information:", self.styles["DrugDeckHeading3"]))  # Updated style name
            
            for package in packaging:
                package_text = f"• Package NDC: {package.get('package_ndc', 'Unknown')}<br/>"
                package_text += f"  Description: {package.get('description', 'Unknown')}<br/>"
                package_text += f"  Marketing Start Date: {package.get('marketing_start_date', 'Unknown')}<br/>"
                package_text += f"  Sample: {'Yes' if package.get('sample', False) else 'No'}"
                result.append(Paragraph(package_text, self.styles["DrugDeckNormal"]))  # Updated style name
                result.append(Spacer(1, 0.05*inch))
        
        return result
    
    def _create_ai_insights_section(self):
        """Create the AI insights section."""
        insights = self.report_data.get("ai_insights", {})
        
        result = []
        
        for key, value in insights.items():
            if value:
                heading = key.replace("_", " ").title()
                result.append(Paragraph(heading, self.styles["DrugDeckHeading3"]))  # Updated style name
                result.append(Paragraph(value, self.styles["DrugDeckNormal"]))  # Updated style name
                result.append(Spacer(1, 0.1*inch))
        
        return result