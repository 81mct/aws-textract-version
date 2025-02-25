import boto3
import psycopg2
import logging
import json

# Configure logging
logging.basicConfig(filename='textract_redshift.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class TextractToRedshift:
    def __init__(self, aws_config, db_config):
        self.aws_config = aws_config
        self.db_config = db_config
        self.textract_client = boto3.client('textract', region_name=self.aws_config['region'])
    
    def extract_text_from_s3(self, bucket, document):
        """Extract text from a document stored in S3 using AWS Textract."""
        try:
            response = self.textract_client.analyze_document(
                Document={'S3Object': {'Bucket': bucket, 'Name': document}},
                FeatureTypes=['TABLES', 'FORMS']
            )
            extracted_text = " ".join([block['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE'])
            return extracted_text
        except Exception as e:
            logging.error(f"Error extracting text from {document}: {e}")
            return None
    
    def connect_to_redshift(self):
        """Establishes connection to Redshift database."""
        try:
            return psycopg2.connect(**self.db_config)
        except Exception as e:
            logging.error(f"Database connection error: {e}")
            return None
    
    def insert_text_into_redshift(self, extracted_text, document_name):
        """Inserts extracted text into Redshift table."""
        query = """
        INSERT INTO extracted_documents (document_name, extracted_text)
        VALUES (%s, %s);
        """
        try:
            with self.connect_to_redshift() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (document_name, extracted_text))
                    conn.commit()
            logging.info(f"Successfully inserted {document_name} into Redshift.")
        except Exception as e:
            logging.error(f"Failed to insert {document_name} into Redshift: {e}")
    
if __name__ == "__main__":
    aws_config = {
        'region': 'us-east-1'
    }
    db_config = {
        'host': 'your-redshift-cluster-endpoint',
        'dbname': 'your_database',
        'user': 'your_user',
        'password': 'your_password',
        'port': '5439'
    }
    
    textract_redshift = TextractToRedshift(aws_config, db_config)
    
    # Example usage
    s3_bucket = 'your-s3-bucket-name'
    document_name = 'example_document.pdf'
    extracted_text = textract_redshift.extract_text_from_s3(s3_bucket, document_name)
    
    if extracted_text:
        textract_redshift.insert_text_into_redshift(extracted_text, document_name)
    else:
        logging.error("No text extracted. Skipping database insertion.")
