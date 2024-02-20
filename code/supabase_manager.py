from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# ADDING A USER TO DATABASE
def add_user_to_soup(user_id: int, username: str, team: str) -> None:
    # Insert user data into Supabase table
    response = supabase.table("users").insert({
        "user_id": user_id,
        "username": username,
        "team": team
    }).execute()

    if response.successful:
        print("User added to the database successfully.")
    else:
        print("Error adding user to the database:", response.error)



# PRINTING DATABASE CONTENT METHOD
def print_database_content() -> None:
    # Retrieve all rows from the "users" table
    response = supabase.table("users").select("*").execute()

    if "data" in response:
        data = response["data"]  # Extract data from the response
        if data:
            print("Database Content:")
            for row in data:
                print(row)
        else:
            print("No data returned from the database.")
    else:
        print("Error fetching data from the database:", response)

# Example usage:
#print_database_content()