import tkinter as tk
import pygubu
from tkinter import messagebox
from typing import Dict, List
import countdown
from networking import Networking
from supabase_manager import supabase, print_database_content, insert_user


# --------------------------------
# CODE FOR UI!
# --------------------------------
networking = Networking()
# Make build_ui_instance a global variable to hold the pygubu.Builder instance
build_ui_instance: pygubu.Builder = pygubu.Builder()



# --------------------------------
# CREATE THE SOCKETS!
# --------------------------------
def createSockets() -> None:
    if networking.setupSockets():
        print("Sockets setup successful.")
    else:
        print("Failed to set up sockets.")
    


# --------------------------------
# WHEN CONTINUE IS CLICKED!
# --------------------------------
def on_continue_clicked(root: tk.Tk, users, input_ids) -> None:
    
    if validate_equipment_ids(input_ids):
        print("Checked")
    else:
        return
    user_data:dict = []
    # Iterate over input IDs to retrieve user information
    for input_id, field_name in input_ids.items():
       if "_user_id_" in input_id:  # Check if the input ID corresponds to user ID
           entry = build_ui_instance.get_object(input_id)
           username_field = input_id.replace("user_id", "username")  # Get corresponding username field ID
           username_entry = build_ui_instance.get_object(username_field)
           user_id = entry.get().strip()
           username = username_entry.get().strip()
           if user_id and username:  # Only append if both user ID and username are not empty
               # Determine the team based on the input ID
               team = "red" if "red" in input_id else "blue"
               user_data.append((user_id, username, team))


   # Insert user data into Supabase table
    for user_id, username, team in user_data:
       # Convert user_id to int (assuming user_id should be an integer)
        try:
           user_id = int(user_id)
        except ValueError:
           messagebox.showerror("Error", "User ID must be a valid number.")
           return


       # Check if user_id already exists in the users table
        query = supabase.table("users").select("user_id").eq("username", username)
        response = query.execute()


       # If user_id already exists, show error message and skip insertion
        if response.data:
           #messagebox.showerror("Error", f"User ID {user_id} already exists.")
           continue
        else:
           # If user_id doesn't exist, add the user to the Supabase table
           insert_user(entry, username, user_id, users, team)
           messagebox.showinfo("Info", f"User ID {user_id} not found, adding to the database.")


   # Notify user of successful insertion
    messagebox.showinfo("Success", "User information inserted successfully.")
   
    # Countdown screen built
    countdown.build(root, user_data, networking)

    

# --------------------------------
# SCREEN BUILDER WITH ALL THE ATTRIBUTES!
# --------------------------------
def builder(root:tk.Tk, users :dict) -> None:
    builder: pygubu.Builder = pygubu.Builder()
    try:
        builder.add_from_file("ui/player_interface.ui")
    except:
        builder.add_from_file("../ui/player_interface.ui")
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
    

# --------------------------------
# CLEAR ENTRY FIELDS!
# --------------------------------
def clear_entry_fields(builder:pygubu.builder):
    print("F12 pressed. Clearing entry fields")

    #Clear all widget contents
    def clear_widgets(widget):
        if isinstance(widget,tk.Entry):
            #clear content
            widget.delete(0,tk.END)
        elif hasattr(widget, 'winfo_children'):
            #recursively traverse over all widget children
            for child_widget in widget.winfo_children(): 
                clear_widgets(child_widget)

    root_widget=builder.get_object("master")
    clear_widgets(root_widget)


# --------------------------------
# BUILD SCREEN!
# --------------------------------
def build_ui(root: tk.Tk, users: dict) -> None:
    global build_ui_instance  # Make sure to use the global instance

    try:
        build_ui_instance.add_from_file("ui/player_interface.ui")
    except:
        build_ui_instance.add_from_file("../ui/player_interface.ui")


    main_frame: tk.Frame = build_ui_instance.get_object("master", root)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    red_frame: tk.Frame = build_ui_instance.get_object("red_team", main_frame)
    blue_frame: tk.Frame = build_ui_instance.get_object("blue_team", main_frame)

    input_ids: Dict[int, str] = {}
    fields: List[str] = {
        "red_equipment_id_",
        "red_user_id_",
        "red_username_",
        "blue_equipment_id_",
        "blue_user_id_",
        "blue_username_"
    }

    for i in range(1, 16):
        for field in fields:
            entry_id = f"{field}{i}"  # Use the ID from XML directly
            entry = build_ui_instance.get_object(entry_id,
                                                 red_frame if "red" in field else blue_frame)
            input_ids[entry_id] = entry_id  # Use the same ID for input_ids
            team="blue" if "blue" in field else "red"
            entry.bind ("<Return>", lambda event, entry=entry, team=team: autofill_username(entry,users,team))


    root.bind("<KeyPress-F5>", lambda event: on_continue_clicked(root, users, input_ids))
    submit_button = build_ui_instance.get_object("submit")
    submit_button.configure(command=lambda: on_continue_clicked(root, users, input_ids))

    # Clear entry fields
    root.bind("<F12>", lambda event: clear_entry_fields(build_ui_instance))


# --------------------------------
# Check that all users have a equipment ID!
# --------------------------------

def validate_equipment_ids(input_ids: Dict[int, str]) -> bool:
    for input_id, field_name in input_ids.items():
        if "_equipment_id_" in field_name:  # we only want to check equipment Id fields
            entry = build_ui_instance.get_object(input_id)
            user_id_field_name = field_name.replace("_equipment_id_", "_user_id_") # swaps field names so we can  check if userID is not empty
            user_id_entry = build_ui_instance.get_object(user_id_field_name)
            user_id = user_id_entry.get().strip() # get value of user_id
            if user_id:  # is empty check
                equipment_id = entry.get().strip()
                if not equipment_id:  # if equipment ID empty return false and show error
                    field_number = field_name.split("_")[-1]
                    messagebox.showerror("Warning", f"Equipment ID for {field_name} cannot be empty.")
                    return False
    return True




# --------------------------------
# AUTOFILL USERNAME WHEN ENTER IS CLICKED!
# --------------------------------
def autofill_username(entry, users, team):
   entry_name = entry.winfo_name()
   print(entry)
   if "_user_id_" in entry_name:  # Check if the input ID corresponds to user ID
    user_id = entry.get().strip()
   if user_id:
       try:
           # Get the parent frame
           parent_frame = entry.master
           while parent_frame.winfo_name() not in {"red_team", "blue_team"}:
               parent_frame = parent_frame.master

           # Determine the team based on the parent frame
           team = "red_team" if parent_frame.winfo_name() == "red_team" else "blue_team"

           # Get the corresponding username entry widget
           username_entry = parent_frame.nametowidget(entry.winfo_name().replace("user_id", "username"))
           if username_entry:
               # Query Supabase to find username based on user ID
               query = supabase.table("users").select("username").eq("user_id", user_id)
               response = query.execute()
               
               # Print the response
               print("Supabase Response:", response)

               # Check if response contains data and retrieve username
               if response and response.data:
                   username = response.data[0]["username"]
                   print("Retrieved username:", username)  # Debugging statement
                   username_entry.delete(0, tk.END)  # Clear existing content
                   username_entry.insert(0, username)
                   print("Username autofilled to widget number:", username_entry.winfo_id())  # Print widget number
                   print("User team attribute:", "red" if "red" in parent_frame.winfo_name() else "blue")  # Print team attribute
                   print("User's team set to:", team)

                   # Update the team attribute of the corresponding user
                   #users[user_id]["team"] = team
                #    update_user_team(user_id, team)

               else:
                   print("No username data found in response.")  # Debugging statement
           else:
               print("Username entry widget not found.")
       except Exception as e:
           print(f"An error occurred: {e}")
