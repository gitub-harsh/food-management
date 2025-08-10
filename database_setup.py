import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('food.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Providers (
    Provider_ID INTEGER PRIMARY KEY,
    Name TEXT,
    Type TEXT,
    Address TEXT,
    City TEXT,
    Contact TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Receivers (
    Receiver_ID INTEGER PRIMARY KEY,
    Name TEXT,
    Type TEXT,
    City TEXT,
    Contact TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS FoodListings (
    Food_ID INTEGER PRIMARY KEY,
    Food_Name TEXT,
    Quantity INTEGER,
    Expiry_Date TEXT,
    Provider_ID INTEGER,
    Provider_Type TEXT,
    Location TEXT,
    Food_Type TEXT,
    Meal_Type TEXT,
    FOREIGN KEY (Provider_ID) REFERENCES Providers(Provider_ID)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Claims (
    Claim_ID INTEGER PRIMARY KEY,
    Food_ID INTEGER,
    Receiver_ID INTEGER,
    Status TEXT,
    Timestamp TEXT,
    FOREIGN KEY (Food_ID) REFERENCES FoodListings(Food_ID),
    FOREIGN KEY (Receiver_ID) REFERENCES Receivers(Receiver_ID)
)
''')

# Load CSV files
providers_df = pd.read_csv('providers_data.csv')
receivers_df = pd.read_csv('receivers_data.csv')
food_df = pd.read_csv('food_listings_data.csv')
claims_df = pd.read_csv('claims_data.csv')

# Insert data
providers_df.to_sql('Providers', conn, if_exists='replace', index=False)
receivers_df.to_sql('Receivers', conn, if_exists='replace', index=False)
food_df.to_sql('FoodListings', conn, if_exists='replace', index=False)
claims_df.to_sql('Claims', conn, if_exists='replace', index=False)

print("Database created and CSV data loaded successfully.")
conn.close()
