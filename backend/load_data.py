import pandas as pd
from sqlalchemy import create_engine
import os
from urllib.parse import quote_plus # <-- ADD THIS IMPORT

# --- Database Connection Details ---
# IMPORTANT: Replace 'your_password' with your PostgreSQL password.
DB_USER = 'postgres'
DB_PASSWORD = 'Abra@6161' # <-- EDIT THIS
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'chatbot_db'

# This will safely encode any special characters in your password.
encoded_password = quote_plus(DB_PASSWORD)

DATABASE_URI = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- Data Loading Logic ---
def load_data_to_db():
    """
    Reads CSV files from the 'data' directory and loads them into the PostgreSQL database.
    """
    try:
        engine = create_engine(DATABASE_URI)
        print("✅ Successfully connected to the database.")
    except Exception as e:
        print(f"❌ Error connecting to the database: {e}")
        return

    # Path to the directory containing the CSV files
    data_dir = 'data'

    # List of CSV files to process
    csv_files = [
        'users.csv',
        'products.csv',
        'orders.csv',
        'order_items.csv',
        'inventory_items.csv',
        'distribution_centers.csv'
    ]

    for file_name in csv_files:
        file_path = os.path.join(data_dir, file_name)

        # The table name will be the file name without the .csv extension
        table_name = os.path.splitext(file_name)[0]

        try:
            print(f"Processing {file_name} -> table '{table_name}'...")

            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(file_path)

            # Write the DataFrame to the SQL database
            # if_exists='replace' will drop the table if it already exists and create a new one.
            df.to_sql(table_name, con=engine, if_exists='replace', index=False)

            print(f"✅ Successfully loaded {len(df)} rows into '{table_name}'.")

        except FileNotFoundError:
            print(f"❌ Error: {file_name} not found in {data_dir}/")
        except Exception as e:
            print(f"❌ An error occurred with {file_name}: {e}")

    print("\n🎉 All data has been loaded into the database.")


if __name__ == '__main__':
    load_data_to_db()