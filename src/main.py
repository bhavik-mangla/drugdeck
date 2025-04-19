import json
import os
import yaml
import logging
import time
from datetime import datetime
from api.fda_client import FDAClient
from api.gemini_client import GeminiClient
from generators.report_generator import ReportGenerator
from generators.pdf_generator import PDFGenerator
from models.drug_model import Drug
from utils.helpers import format_ndc
from dotenv import load_dotenv

# Configure logging
def setup_logging(log_level=logging.INFO):
    """
    Set up logging configuration.
    
    Args:
        log_level: Logging level (default: INFO)
    """
    # Ensure logs directory exists
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Generate timestamp for log filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/drugdeck_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger('drugdeck')

def load_config():
    """Load application configuration."""
    logger = logging.getLogger('drugdeck')
    try:
        with open('config/config.yaml', 'r') as file:
            logger.info("Configuration loaded successfully")
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        # Provide default configuration
        logger.info("Using default configuration")
        return {
            "google_api_key": os.getenv("GOOGLE_API_KEY", "AIzaSyBh6L4A1RqEBpMdocsZ9cNWDUTYstDEDuE"),
            "data_file": "data/drug-ndc.json",
            "output_dir": "reports"
        }

def ensure_output_dir(dir_path):
    """Ensure output directory exists."""
    logger = logging.getLogger('drugdeck')
    if not os.path.exists(dir_path):
        logger.info(f"Creating output directory: {dir_path}")
        os.makedirs(dir_path)
    else:
        logger.info(f"Output directory already exists: {dir_path}")

def main():
    # Setup logging
    logger = setup_logging()
    logger.info("======= DrugDeck Application Started =======")
    start_time = time.time()
    
    # Load environment variables
    load_dotenv()
    logger.info("Environment variables loaded")
    
    # Load configuration
    config = load_config()
    google_api_key = config.get('google_api_key')
    output_dir = config.get('output_dir', 'reports')
    
    # Ensure output directory exists
    ensure_output_dir(output_dir)
    
    # Get NDC code from user
    ndc_code = input("Enter the NDC code: ")
    original_ndc = ndc_code
    ndc_code = format_ndc(ndc_code)
    
    logger.info(f"Processing NDC: {ndc_code} (original input: {original_ndc})")
    print(f"Searching for drug with NDC: {ndc_code}")
    
    # Initialize FDA client and fetch drug info
    logger.info("Initializing FDA client")
    fda_client = FDAClient('data/drug-ndc.json')
    
    logger.info(f"Fetching drug information for NDC: {ndc_code}")
    timer_start = time.time()
    drug_info = fda_client.get_drug_info(ndc_code)
    logger.info(f"Drug info fetch completed in {time.time() - timer_start:.2f} seconds")
    
    if not drug_info:
        logger.error(f"No drug information found for NDC: {ndc_code}")
        print("No drug information found for the provided NDC code.")
        return
    
    # Create drug model
    drug = Drug(ndc_code, drug_info)
    logger.info(f"Drug model created: {drug.brand_name} ({drug.generic_name})")
    print(f"Found drug: {drug.brand_name} ({drug.generic_name})")
    
    # Fetch additional data
    print("Fetching FDA label information...")
    logger.info("Fetching FDA label information")
    timer_start = time.time()
    label_info = fda_client.get_drug_label(ndc_code)
    logger.info(f"FDA label fetch completed in {time.time() - timer_start:.2f} seconds")
    
    if label_info:
        logger.info("FDA label information retrieved successfully")
    else:
        logger.warning("No FDA label information found")
    
    # Initialize Gemini client and generate AI insights
    logger.info("Setting up AI insights")
    
    # In a production environment, we would use this code:
    # print("Generating AI insights...")
    # logger.info("Initializing Gemini client and generating AI insights")
    # timer_start = time.time()
    # gemini_client = GeminiClient(google_api_key)
    # ai_insights = gemini_client.get_ai_insights(drug_info)
    # logger.info(f"AI insights generation completed in {time.time() - timer_start:.2f} seconds")
    
    # For now, using placeholder data
    ai_insights = {
        "drug_summary": "This is a summary of the drug.",
        "mechanism_of_action": "This is the mechanism of action.",
        "side_effects": "These are the side effects.",
        "market_trends": "These are the market trends.",
        "patient_journey": "This is the patient journey."
    }
    logger.info("Placeholder AI insights created")
    
    # Compile report
    print("Compiling report...")
    logger.info("Compiling report")
    timer_start = time.time()
    report_generator = ReportGenerator(drug_info, ai_insights, label_info)
    report = report_generator.compile_report(ndc_code)
    logger.info(f"Report compilation completed in {time.time() - timer_start:.2f} seconds")
    
    # Generate PDF
    output_file = os.path.join(output_dir, f"{ndc_code}_drug_report.pdf")
    print(f"Generating PDF report: {output_file}")
    logger.info(f"Generating PDF report: {output_file}")
    
    timer_start = time.time()
    pdf_generator = PDFGenerator(report, output_file)
    pdf_generator.generate_pdf()
    logger.info(f"PDF generation completed in {time.time() - timer_start:.2f} seconds")
    
    print(f"Drug report generated successfully: {output_file}")
    logger.info(f"Drug report generated successfully: {output_file}")
    
    # Optionally save JSON data
    json_output = os.path.join(output_dir, f"{ndc_code}_drug_report.json")
    with open(json_output, 'w') as f:
        json.dump(report, f, indent=2)
    logger.info(f"JSON data saved: {json_output}")
    print(f"JSON data saved: {json_output}")
    
    # Log execution time
    total_time = time.time() - start_time
    logger.info(f"Total execution time: {total_time:.2f} seconds")
    logger.info("======= DrugDeck Application Completed =======")

if __name__ == "__main__":
    main()