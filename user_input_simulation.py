import psycopg2
import logging

# Configure logging
logging.basicConfig(filename='user_input_simulation.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class UserInputSimulation:
    def __init__(self, db_config):
        self.db_config = db_config
    
    def connect_db(self):
        """Establishes a connection to the RDS database."""
        try:
            return psycopg2.connect(**self.db_config)
        except Exception as e:
            logging.error(f"Database connection error: {e}")
            return None
    
    def insert_user_data(self, user_data):
        """Inserts user-entered data into the database."""
        query = """
        INSERT INTO users (first_name, last_name, middle_name, zipcode, dateofbirth, idcardnumber, idcardissuedate, idcardexpirationdate)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            with self.connect_db() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (
                        user_data['first_name'], user_data['last_name'], user_data['middle_name'],
                        user_data['zipcode'], user_data['dateofbirth'], user_data['idcardnumber'],
                        user_data['idcardissuedate'], user_data['idcardexpirationdate']
                    ))
                    conn.commit()
            logging.info(f"Successfully inserted user: {user_data['first_name']} {user_data['last_name']}.")
        except Exception as e:
            logging.error(f"Failed to insert user data: {e}")
    
if __name__ == "__main__":
    db_config = {
        'host': 'your-rds-endpoint',
        'dbname': 'your_database',
        'user': 'your_user',
        'password': 'your_password',
        'port': '5432'
    }
    
    simulator = UserInputSimulation(db_config)
    
    # Simulating user input
    user_data = {
        'first_name': input("Enter First Name: "),
        'last_name': input("Enter Last Name: "),
        'middle_name': input("Enter Middle Name (or leave blank): ") or None,
        'zipcode': input("Enter ZIP Code: "),
        'dateofbirth': input("Enter Date of Birth (YYYY-MM-DD): "),
        'idcardnumber': input("Enter ID Card Number: "),
        'idcardissuedate': input("Enter ID Issue Date (YYYY-MM-DD): "),
        'idcardexpirationdate': input("Enter ID Expiration Date (YYYY-MM-DD): ")
    }
    
    simulator.insert_user_data(user_data)
    print("✅ User data successfully stored in the database!")
