import os
if not os.path.exists('food.db'):
    
    import database_setup
import streamlit as st

import sqlite3
import pandas as pd
from queries import (
    providers_receivers_per_city, top_provider_type, providers_contact_by_city,
    top_receivers, total_food_quantity, city_with_most_listings, most_common_food_types,
    claims_per_food_item, top_provider_by_claims, claim_status_percentage,
    avg_quantity_per_receiver, most_claimed_meal_type, total_donated_by_provider,
    expired_food_items, top_cities_by_quantity
)

st.set_page_config(page_title="Local Food Wastage Management System", layout="wide")
st.title("Local Food Wastage Management System")

# Database connection helper
def get_conn():
    return sqlite3.connect('food.db', check_same_thread=False)

conn = get_conn()

# Sidebar menu
menu = ["Home", "View Data", "Add Data", "Update Data", "Delete Data", "Analysis"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.markdown(
    """
    ### Project Overview
    This Streamlit app demonstrates the Local Food Wastage Management System.
    Use the menu to view tables, perform CRUD operations, and run analysis (15 queries).
    """
    )

# 1. View Data
if choice == "View Data":
    table = st.selectbox("Select Table", ["Providers", "Receivers", "FoodListings", "Claims"])
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    st.dataframe(df)

# 2. Add Data
elif choice == "Add Data":
    st.subheader("Add New Provider/Receiver/FoodListing/Claim")
    entity = st.selectbox("Entity to add", ["Provider", "Receiver", "FoodListing", "Claim"])

    if entity == "Provider":
        name = st.text_input("Name")
        type_ = st.text_input("Type")
        address = st.text_input("Address")
        city = st.text_input("City")
        contact = st.text_input("Contact")
        if st.button("Add Provider"):
            conn.execute("INSERT INTO Providers (Name, Type, Address, City, Contact) VALUES (?, ?, ?, ?, ?)",
                         (name, type_, address, city, contact))
            conn.commit()
            st.success("Provider added successfully!")

    if entity == "Receiver":
        name = st.text_input("Name (Receiver)")
        type_ = st.text_input("Type (Receiver)")
        city = st.text_input("City (Receiver)")
        contact = st.text_input("Contact (Receiver)")
        if st.button("Add Receiver"):
            conn.execute("INSERT INTO Receivers (Name, Type, City, Contact) VALUES (?, ?, ?, ?)",
                         (name, type_, city, contact))
            conn.commit()
            st.success("Receiver added successfully!")

    if entity == "FoodListing":
        food_id = st.number_input("Food ID (unique)", step=1, value=0)
        food_name = st.text_input("Food Name")
        quantity = st.number_input("Quantity", step=1, value=1)
        expiry = st.text_input("Expiry Date (YYYY-MM-DD)")
        provider_id = st.number_input("Provider ID", step=1, value=0)
        provider_type = st.text_input("Provider Type")
        location = st.text_input("Location/City")
        food_type = st.text_input("Food Type")
        meal_type = st.text_input("Meal Type")
        if st.button("Add Food Listing"):
            conn.execute("""INSERT OR REPLACE INTO FoodListings
                         (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""" ,
                         (food_id if food_id!=0 else None, food_name, quantity, expiry, provider_id if provider_id!=0 else None, provider_type, location, food_type, meal_type))
            conn.commit()
            st.success("Food listing added successfully!")

    if entity == "Claim":
        claim_id = st.number_input("Claim ID (unique)", step=1, value=0)
        food_id = st.number_input("Food ID", step=1, value=0, key="claim_food")
        receiver_id = st.number_input("Receiver ID", step=1, value=0, key="claim_receiver")
        status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"])
        timestamp = st.text_input("Timestamp (YYYY-MM-DD HH:MM:SS)")
        if st.button("Add Claim"):
            conn.execute("INSERT OR REPLACE INTO Claims (Claim_ID, Food_ID, Receiver_ID, Status, Timestamp) VALUES (?, ?, ?, ?, ?)",
                         (claim_id if claim_id!=0 else None, food_id if food_id!=0 else None, receiver_id if receiver_id!=0 else None, status, timestamp))
            conn.commit()
            st.success("Claim added successfully!")

# 3. Update Data
elif choice == "Update Data":
    st.subheader("Update Food Quantity or Claim Status")
    update_entity = st.selectbox("Update", ["Food Quantity", "Claim Status"])
    if update_entity == "Food Quantity":
        food_id = st.number_input("Food ID", step=1)
        quantity = st.number_input("New Quantity", step=1)
        if st.button("Update Quantity"):
            conn.execute("UPDATE FoodListings SET Quantity=? WHERE Food_ID=?", (quantity, food_id))
            conn.commit()
            st.success("Quantity updated successfully!")
    else:
        claim_id = st.number_input("Claim ID", step=1)
        status = st.selectbox("New Status", ["Pending", "Completed", "Cancelled"])
        if st.button("Update Claim"):
            conn.execute("UPDATE Claims SET Status=? WHERE Claim_ID=?", (status, claim_id))
            conn.commit()
            st.success("Claim updated successfully!")

# 4. Delete Data
elif choice == "Delete Data":
    st.subheader("Delete Records")
    del_entity = st.selectbox("Delete from", ["Providers", "Receivers", "FoodListings", "Claims"])
    id_to_delete = st.number_input("ID to delete", step=1)
    if st.button("Delete"):
        mapping = {"Providers":"Provider_ID","Receivers":"Receiver_ID","FoodListings":"Food_ID","Claims":"Claim_ID"}
        conn.execute(f"DELETE FROM {del_entity} WHERE {mapping[del_entity]}=?", (id_to_delete,))
        conn.commit()
        st.success(f"Deleted {del_entity} record with id {id_to_delete}")

# 5. Analysis (All 15 queries)
elif choice == "Analysis":
    st.subheader("Data Analysis Results (15 queries)")

    st.write('Providers and Receivers per City')
    st.dataframe(providers_receivers_per_city())

    st.write('Top Provider Types')
    st.dataframe(top_provider_type())

    city_filter = st.text_input("Enter city for provider contacts (query 3)")
    if city_filter:
        st.write(f"Provider Contacts in {city_filter}")
        st.dataframe(providers_contact_by_city(city_filter))

    st.write('Top Receivers by Claims')
    st.dataframe(top_receivers())

    st.write('Total Food Quantity')
    st.dataframe(total_food_quantity())

    st.write('City with Most Listings')
    st.dataframe(city_with_most_listings())

    st.write('Most Common Food Types')
    st.dataframe(most_common_food_types())

    st.write('Claims per Food Item')
    st.dataframe(claims_per_food_item())

    st.write('Top Providers by Successful Claims')
    st.dataframe(top_provider_by_claims())

    st.write('Claim Status Percentage')
    st.dataframe(claim_status_percentage())

    st.write('Average Quantity per Receiver')
    st.dataframe(avg_quantity_per_receiver())

    st.write('Most Claimed Meal Type')
    st.dataframe(most_claimed_meal_type())

    st.write('Total Donated by Provider')
    st.dataframe(total_donated_by_provider())

    date_filter = st.text_input("Enter current date (YYYY-MM-DD) for expired items (query 14)")
    if date_filter:
        st.write(f"Expired Food Items before {date_filter}")
        st.dataframe(expired_food_items(date_filter))

    st.write('Top Cities by Quantity')
    st.dataframe(top_cities_by_quantity())

# Streamlit will manage lifecycle; explicit close if needed
