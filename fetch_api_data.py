import requests
import pandas as pd
from sqlalchemy import create_engine
import sys

# --- CONFIGURATION ---
DB_USER = "root"          
DB_PASSWORD = 9887992780  
DB_HOST = "localhost"
DB_NAME = "dev_analytics"

# Codeforces API endpoint for public contests
API_URL = "https://codeforces.com/api/contest.list?gym=false"

def fetch_data_from_api(url):
    """EXTRACT: Fetch JSON data from the REST API."""
    print("Fetching data from Codeforces API...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raises an error for bad HTTP status codes (e.g., 404, 500)
        
        # The API returns a JSON object where the actual data is inside the 'result' key
        json_data = response.json()
        
        if json_data['status'] == 'OK':
            print(f"✅ Successfully fetched {len(json_data['result'])} records.")
            return json_data['result']
        else:
            print("❌ API returned a non-OK status.")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API Request failed: {e}")
        sys.exit(1)

def process_json_data(raw_json):
    """TRANSFORM: Parse the JSON and format it using Pandas."""
    print("Processing and cleaning JSON data...")
    
    # Load JSON directly into a Pandas DataFrame
    df = pd.DataFrame(raw_json)
    
    # 1. Select only the columns we care about
    columns_to_keep = ['id', 'name', 'type', 'phase', 'durationSeconds']
    df = df[columns_to_keep]
    
    # 2. Transform Data: Convert duration from seconds to hours for better readability
    df['duration_hours'] = round(df['durationSeconds'] / 3600, 2)
    
    # 3. Drop the old seconds column
    df = df.drop(columns=['durationSeconds'])
    
    # 4. Filter: Let's only keep contests that have 'FINISHED'
    df = df[df['phase'] == 'FINISHED']
    
    return df

def load_data_to_db(df, db_user, db_password, db_host, db_name):
    """LOAD: Insert the processed data into MySQL."""
    print("Loading data into MySQL...")
    
    connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
    
    try:
        engine = create_engine(connection_string)
        
        # Insert data into a table named 'coding_contests'. Replace if it already exists.
        df.to_sql('coding_contests', con=engine, if_exists='replace', index=False)
        print("✅ Data successfully saved to the database!")
        
    except Exception as e:
        print(f"❌ Database error: {e}")

# --- EXECUTION FLOW ---
if __name__ == "__main__":
    # 1. Fetch
    raw_data = fetch_data_from_api(API_URL)
    
    # 2. Process
    processed_df = process_json_data(raw_data)
    
    # 3. Load
    load_data_to_db(processed_df, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)