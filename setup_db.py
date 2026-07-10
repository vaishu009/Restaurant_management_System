import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Vaishu@123')
}

def setup_database():
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Create database if not exists (though Railway already created it)
        # Instead, let's just use the existing DB from env var
        database_name = os.getenv('DB_NAME', 'restaurant_management')
        cursor.execute(f'USE {database_name}')

        # Clear only master data to avoid duplicates while preserving history
        print('Cleaning up master data (Menu, Categories)...')
        cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
        # We do NOT truncate Orders, Payments, or Customers to preserve history
        tables_to_refresh = ['Menu_Items', 'Categories', 'Restaurant_Tables']
        for table in tables_to_refresh:
            try:
                cursor.execute(f'TRUNCATE TABLE {table}')
            except:
                pass  # Ignore if table doesn't exist yet
        cursor.execute('SET FOREIGN_KEY_CHECKS = 1')

        # Read and execute Tables.sql
        print('Creating tables...')
        with open('Tables.sql', 'r') as f:
            sql_commands = f.read().split(';')
            for command in sql_commands:
                command = command.strip()
                if command and not command.startswith('use') and not command.startswith('select'):
                    try:
                        cursor.execute(command)
                    except mysql.connector.Error as err:
                        if 'already exists' in str(err):
                            continue
                        print(f'Error executing command: {err}')

        # Read and execute insert_data.sql
        print('Inserting sample data...')
        with open('insert_data.sql', 'r') as f:
            sql_commands = f.read().split(';')
            for command in sql_commands:
                command = command.strip()
                if command and not command.startswith('use'):
                    try:
                        cursor.execute(command)
                    except mysql.connector.Error as err:
                        if 'Duplicate entry' in str(err):
                            continue
                        print(f'Error executing command: {err}')

        conn.commit()
        print('Database setup completed successfully!')
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f'Error: {err}')

if __name__ == '__main__':
    setup_database()
