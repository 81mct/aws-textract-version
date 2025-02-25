import os
import io
import cv2
import numpy as np
import pytesseract
from PIL import Image
import psycopg2

# Configure Tesseract path (Update this to match your installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ImagePreprocessor:
    def __init__(self, image):
        self.image = image

    def resize(self, factor=2):
        width, height = self.image.size
        new_size = (int(width * factor), int(height * factor))
        self.image = self.image.resize(new_size, Image.Resampling.LANCZOS)
        return self

    def threshold(self):
        gray_image = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2GRAY)
        _, thresh_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
        self.image = Image.fromarray(thresh_image)
        return self

def extract_text(image_path):
    image = Image.open(image_path)
    preprocessor = ImagePreprocessor(image).resize().threshold()
    text = pytesseract.image_to_string(preprocessor.image, lang='eng')
    return text

def get_value_from_txt(text_file_path, category):
    if not os.path.exists(text_file_path):
        print(f"Text file {text_file_path} not found.")
        return None
    
    with open(text_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        for line in content.splitlines():
            if line.lower().startswith(f'{category.lower()}:'):
                return line.split(':', 1)[1].strip().lower()
    return None

def insert_into_local_db(data):
    conn_string = "dbname='local_db' user='user' password='password' host='localhost' port='5432'"
    try:
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                insert_stmt = """
                    INSERT INTO id_information
                    (last_name, first_name, middle_name, dob, id_number, zip_code, issue_date, expiration_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(insert_stmt, (
                    data['Last Name'],
                    data['First Name'],
                    data['Middle Name'],
                    data['DOB'],
                    data['ID Number'],
                    data['Zip Code'],
                    data['Issue Date'],
                    data['Expiration Date']
                ))
                conn.commit()
                print("Data inserted successfully into local database.")
    except Exception as e:
        print(f"Database insertion failed: {e}")

if __name__ == "__main__":
    image_path = 'uploads/sample_id.jpg'  # Update with actual image file
    text_file_path = 'uploads/sample_id.txt'  # Update with actual text file
    
    categories = [
        "Last Name", "First Name", "Middle Name", "DOB", "ID Number", "Zip Code", "Issue Date", "Expiration Date"
    ]
    
    extracted_text = extract_text(image_path)
    
    matched_data = {}
    for category in categories:
        txt_value = get_value_from_txt(text_file_path, category)
        if txt_value and txt_value.lower() in extracted_text.lower():
            matched_data[category] = txt_value
            print(f"Matched {category}: {txt_value}")
        else:
            print(f"No match found for {category}")
    
    if matched_data:
        insert_into_local_db(matched_data)
    else:
        print("No data matched for insertion.")
