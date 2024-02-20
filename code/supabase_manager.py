from dotenv import load_dotenv
import os
# from supabase import create_client
from supabase_py import create_client

load_dotenv()

# Initialize Supabase client
supabase_url = 'https://pdfbshphnccebqdnhawd.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBkZmJzaHBobmNjZWJxZG5oYXdkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDgzNjE4OTMsImV4cCI6MjAyMzkzNzg5M30.ZYfCEZfUHuOVlMqDLIkSEA7_PU4B5OHWD-CUGjwfYI8'
supabase = create_client(supabase_url, supabase_key)

response = supabase.table("users").select("*").execute()

# Print the response data to inspect the results
print(response)

# Check if the response contains any data
# if response.get('status') == '200':
#     data = response.get('data')
#     if data:
#         print("Data found:", data)
#     else:
#         print("No data found")
# else:
#     print("Error:", response.get('error'))

new_user_data = {
    'user_id': 1,
    'username': 'john_doe',
}


# ADDING A USER TO DATABASE
def add_user_to_soup(user_id, username):
    # Perform the operation to add user to your Supabase table
    response = supabase.table("users").insert({
        'user_id': user_id,
        'username': username,
    }).execute()

    # Check if the response indicates success
    if response.get('status') == 201:
        print("User added successfully")
    else:
        print("Error adding user:", response.get('error'))


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