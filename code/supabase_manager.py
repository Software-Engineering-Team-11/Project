from dotenv import load_dotenv
import os
from supabase import create_client

# Load environment variables from .env file
load_dotenv()

# Retrieve Supabase URL and key from environment variables
url = "https://pdfbshphnccebqdnhawd.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBkZmJzaHBobmNjZWJxZG5oYXdkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDgzNjE4OTMsImV4cCI6MjAyMzkzNzg5M30.ZYfCEZfUHuOVlMqDLIkSEA7_PU4B5OHWD-CUGjwfYI8"

print("URL:", url)
print("Key:", key)

# Check if the URL or key is missing
if url is None or key is None:
    raise ValueError("Supabase URL or key not found in environment variables.")

# Create Supabase client
supabase = create_client(url, key)

# Function to insert user into "users" table
from postgrest.exceptions import APIError

# --------------------------------
# INSERT USER TO SUPABASE!
# --------------------------------
def insert_user(entry, username, user_id, users, team=None):
   # Define the data to be inserted
   data = {'username': username, 'user_id': user_id}


   # Insert data into "users" table
   try:
       response = supabase.table('users').insert(data).execute()
       print("User inserted successfully.")
       # Set the team attribute if provided
       if team:
           print(f"User's team set to: {team}")
   except APIError as e:
       if e.code == '23505':
           print(f"Failed to insert user: {e.message}")
       else:
           print("Failed to insert user due to an unknown error.")
           print(e)


   print("User attributes:", data)  # Print user attributes


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

