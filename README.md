# drugdeck
Deep research for pharma

## Overview
The drugdeck project is designed to generate comprehensive drug reports based on specific NDC codes. It integrates data from a local JSON file and enhances the reports with AI-generated insights from the Gemini API.

## Features
- Fetch drug information from `drug-ndc.json` based on NDC codes.
- Integrate with the Gemini API for AI-generated insights.
- Generate structured reports and export them in PDF format.

## Project Structure
```
drugdeck
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── fda_client.py
│   │   └── gemini_client.py
│   ├── data
│   │   ├── __init__.py
│   │   └── data_loader.py
│   ├── generators
│   │   ├── __init__.py
│   │   ├── report_generator.py
│   │   └── pdf_generator.py
│   ├── models
│   │   ├── __init__.py
│   │   └── drug_model.py
│   └── utils
│       ├── __init__.py
│       └── helpers.py
├── config
│   └── config.yaml
├── data
│   └── drug-ndc.json
├── tests
│   ├── __init__.py
│   ├── test_fda_client.py
│   ├── test_gemini_client.py
│   └── test_report_generator.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd drugdeck
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Set up your environment variables in a `.env` file based on the `.env.example` provided.
2. Run the application:
   ```
   python src/main.py
   ```
3. Follow the prompts to enter the desired NDC code and generate the drug report.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.