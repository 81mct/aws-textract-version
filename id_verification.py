import psycopg2
import logging
import re
from datetime import datetime
from difflib import SequenceMatcher

# Configure logging
logging.basicConfig(filename='id_verification.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class IDVerification:
    def __init__(self, db_config):
        self.db_config = db_config
    
    def connect_db(self):
        """Establishes a connection to the database."""
        try:
            return psycopg2.connect(**self.db_config)
        except Exception as e:
            logging.error(f"Database connection error: {e}")
            return None
    
    def fetch_user_data(self, filename):
        """Fetches user data from the database based on the given filename."""
        query = '''SELECT first_name, last_name, middle_name, zipcode, dateofbirth, 
                          idcardnumber, idcardissuedate, idcardexpirationdate 
                   FROM users WHERE filename = %s'''
        try:
            with self.connect_db() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (filename,))
                    data = cur.fetchone()
            
            if data:
                return dict(zip(['first_name', 'last_name', 'middle_name', 'zipcode',
                                 'dateofbirth', 'idcardnumber', 'idcardissuedate', 'idcardexpirationdate'], data))
            else:
                logging.error(f"No data found for filename: {filename}")
                return None
        except Exception as e:
            logging.error(f"Error fetching data for filename {filename}: {e}")
            return None
    
    @staticmethod
    def is_close_match(str1, str2, threshold=0.95):
        """Checks if two strings are similar based on a given threshold."""
        return SequenceMatcher(None, str1.strip(), str2.strip()).ratio() >= threshold
    
    def match_data_with_text_file(self, data, file_path):
        """Matches database data with extracted text file content."""
        try:
            with open(file_path, 'r') as file:
                content = " ".join(file.read().split())  # Normalize spaces

            mismatches = []
            for key, value in data.items():
                if value and key in ['first_name', 'last_name', 'middle_name']:
                    if not self.is_close_match(value, content, 0.95):
                        mismatches.append(f"{key} mismatch: {value}")
                elif key in ['zipcode', 'idcardnumber'] and str(value) not in content:
                    mismatches.append(f"{key} mismatch: {value}")
                elif key in ['dateofbirth', 'idcardissuedate', 'idcardexpirationdate']:
                    if not any(self.is_close_match(value, content, 0.95)):
                        mismatches.append(f"{key} mismatch: {value}")
            
            if mismatches:
                raise ValueError("Data mismatch errors: " + ", ".join(mismatches))
            return True
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            return None

if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'database': 'TestIDVerificationDB',
        'user': 'postgres',
        'password': 'DBpassword'
    }
    
    verifier = IDVerification(db_config)
    filename = 'test_user.txt'
    file_path = 'path/to/extracted_text.txt'
    
    user_data = verifier.fetch_user_data(filename)
    if user_data:
        match_result = verifier.match_data_with_text_file(user_data, file_path)
        print("Data matched successfully!" if match_result else "Data mismatches found.")
    else:
        print("No data found for matching.")
