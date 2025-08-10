import sqlite3
import pandas as pd

def run_query(query):
    conn = sqlite3.connect('food.db')
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def providers_receivers_per_city():
    return run_query("""
    SELECT City, 
           (SELECT COUNT(*) FROM Providers p WHERE p.City = pr.City) AS Provider_Count,
           (SELECT COUNT(*) FROM Receivers r WHERE r.City = pr.City) AS Receiver_Count
    FROM Providers pr
    GROUP BY City
    """)

def top_provider_type():
    return run_query("""
    SELECT Provider_Type, COUNT(*) AS Total_Food_Items
    FROM FoodListings
    GROUP BY Provider_Type
    ORDER BY Total_Food_Items DESC
    """)

def providers_contact_by_city(city):
    return run_query(f"""
    SELECT Name, Contact FROM Providers WHERE City = '{city}'
    """)

def top_receivers():
    return run_query("""
    SELECT r.Name, COUNT(c.Claim_ID) AS Claims_Made
    FROM Claims c
    JOIN Receivers r ON c.Receiver_ID = r.Receiver_ID
    GROUP BY r.Name
    ORDER BY Claims_Made DESC
    """)

def total_food_quantity():
    return run_query("""
    SELECT SUM(Quantity) AS Total_Quantity FROM FoodListings
    """)

def city_with_most_listings():
    return run_query("""
    SELECT Location, COUNT(*) AS Listing_Count
    FROM FoodListings
    GROUP BY Location
    ORDER BY Listing_Count DESC
    """)

def most_common_food_types():
    return run_query("""
    SELECT Food_Type, COUNT(*) AS Count
    FROM FoodListings
    GROUP BY Food_Type
    ORDER BY Count DESC
    """)

def claims_per_food_item():
    return run_query("""
    SELECT f.Food_Name, COUNT(c.Claim_ID) AS Claims_Count
    FROM Claims c
    JOIN FoodListings f ON c.Food_ID = f.Food_ID
    GROUP BY f.Food_Name
    ORDER BY Claims_Count DESC
    """)

def top_provider_by_claims():
    return run_query("""
    SELECT p.Name, COUNT(c.Claim_ID) AS Successful_Claims
    FROM Claims c
    JOIN FoodListings f ON c.Food_ID = f.Food_ID
    JOIN Providers p ON f.Provider_ID = p.Provider_ID
    WHERE c.Status = 'Completed'
    GROUP BY p.Name
    ORDER BY Successful_Claims DESC
    """)

def claim_status_percentage():
    return run_query("""
    SELECT Status,
           ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Claims)), 2) AS Percentage
    FROM Claims
    GROUP BY Status
    """)

def avg_quantity_per_receiver():
    return run_query("""
    SELECT r.Name, AVG(f.Quantity) AS Avg_Quantity
    FROM Claims c
    JOIN Receivers r ON c.Receiver_ID = r.Receiver_ID
    JOIN FoodListings f ON c.Food_ID = f.Food_ID
    GROUP BY r.Name
    """)

def most_claimed_meal_type():
    return run_query("""
    SELECT f.Meal_Type, COUNT(c.Claim_ID) AS Claims_Count
    FROM Claims c
    JOIN FoodListings f ON c.Food_ID = f.Food_ID
    GROUP BY f.Meal_Type
    ORDER BY Claims_Count DESC
    """)

def total_donated_by_provider():
    return run_query("""
    SELECT p.Name, SUM(f.Quantity) AS Total_Donated
    FROM FoodListings f
    JOIN Providers p ON f.Provider_ID = p.Provider_ID
    GROUP BY p.Name
    ORDER BY Total_Donated DESC
    """)

def expired_food_items(current_date):
    return run_query(f"""
    SELECT Food_Name, Expiry_Date
    FROM FoodListings
    WHERE DATE(Expiry_Date) < DATE('{current_date}')
    """)

def top_cities_by_quantity():
    return run_query("""
    SELECT Location, SUM(Quantity) AS Total_Quantity
    FROM FoodListings
    GROUP BY Location
    ORDER BY Total_Quantity DESC
    """)
