import tkinter as tk
import pygubu
from tkinter import messagebox
from typing import Dict, List
from supabase_manager import supabase, print_database_content, add_user_to_soup

def on_continue_clicked(root:tk.Tk,users, input_ids) -> None:
    print('submitted');
     
    if (len(users.get("blue", [])) < 1) or (len(users.get("red", [])) < 1):
    #if (len(users["blue"]) < 1) or (len(users["red"]) < 1):
        messagebox.showerror("Error", "There must be at least 1 user on each team")
        return
     
    for team in users.values():
        for user in team:
            # Get the entered username and ID
            username = user.username_entry.get()
            user_id = user.user_id_entry.get()
            # If username is not entered, skip
            if not username:
                continue
            # Check if the username already exists in the database
            existing_user_id = get_user_id_from_supabase(username)
            if existing_user_id:
                # Display existing user ID
                user.user_id_entry.delete(0, tk.END)  # Clear the entry field
                user.user_id_entry.insert(0, existing_user_id)  # Insert existing ID
            else:
                # Add new user to Supabase
                add_user_to_soup(user_id, username, user.team)

    print("HEY!")

def get_user_id_from_supabase(username: str) -> int:
    # Query the database for the user ID based on the username
    # Implement this function to retrieve user ID from Supabase
    # Return the user ID if found, or None if not found
    pass  # Placeholder, replace with actual implementation

def builder(root:tk.Tk, users :dict) -> None:
    builder: pygubu.Builder = pygubu.Builder()
    try:
        builder.add_from_file("/Users/rafaelbalassiano/Desktop/LASER_TAG/Project/ui/player_interface.ui")
    except:
        builder.add_from_file("/Users/rafaelbalassiano/Desktop/LASER_TAG/Project//ui/player_interface.ui")
    builder.add_from_file("/Users/rafaelbalassiano/Desktop/Laser_Tag/Project/ui/player_interface.ui")

    # Place the main frame in the center of the root window
    # make unresizable
    main_frame: tk.Frame = builder.get_object("master", root)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Create frames for the teams
    teams_frame: tk.Frame = builder.get_object("teams", main_frame)
    red_frame: tk.Frame = builder.get_object("red_team", teams_frame)
    blue_frame: tk.Frame = builder.get_object("blue_team", teams_frame)

    # Create a dictionary of  IDs and corresponding entry field IDs
    input_ids: Dict[int, str] = {}
    fields: List[str] = {
        "red_equipment_id_",
        "red_user_id_",
        "red_username_",
        "blue_equipment_id_",
        "blue_user_id_",
        "blue_username_"
    }

    # Add each entry field ID to the dictionary of entry field IDs
    for i in range(1, 16):
        for field in fields:
            input_ids[builder.get_object(f"{field}{i}", red_frame if "red" in field else blue_frame).winfo_id()] = f"{field}{i}"
    
    print(input_ids)

    #  Place focus on the first entry field
    # builder.get_object("blue_equipment_id_1", blue_frame).focus_set()

    # Testing submit button
    builder.get_object("submit").configure(command=lambda: on_continue_clicked(root,users,input_ids))

    #PRINTING DATABASE CONTENT
    data = supabase.table("users").select("*").execute()
    print("Database Content:")
    print(data)
    print_database_content()
    
