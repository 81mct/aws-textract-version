# AWS Textract Version - ID Processing

## Overview
This module processes ID images using **AWS Textract**, extracts relevant text fields, and sends them to various databases for storage and verification.

## Prerequisites
Before running these scripts, ensure you have:
- **AWS CLI configured** (`aws configure`)
- **An AWS account** with Textract, RDS, and Redshift access
- **Python 3.8+** installed
- Required dependencies (`boto3`, `psycopg2`, `pandas`, `opencv-python`, `pytesseract`, `PIL`)

## Installation
### 1. Clone the Repository
```sh
 git clone https://github.com/81mct/Flask-Tesseract-ID-Verification.git
 cd Flask-Tesseract-ID-Verification/aws_textract_version
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

## Scripts & Functionality
### 1. `id_verification.py`
Extracts text from ID images using AWS Textract and compares with stored values.

### 2. `textract_to_rds.py`
Processes extracted text and inserts it into an **RDS** database.

### 3. `textract_to_redshift.py`
Processes extracted text and inserts it into **Amazon Redshift** for scalable storage and analysis.

### 4. `textract_utils.py`
Contains helper functions for text extraction, image preprocessing, and validation.

### 5. `user_input_simulation.py`
Generates and simulates user input data for testing verification processes.

## Running the Textract Extraction
```sh
python id_verification.py
```

## Contributing
Pull requests are welcome! Open an issue for major changes.

## License
This project is licensed under the **MIT License** - see the LICENSE file for details.

