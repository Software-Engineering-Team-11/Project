import tkinter as tk
import pygubu
from tkinter import messagebox
from typing import Dict, List
import countdown
from users import User
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
        print("\nSockets setup successful.\n")
    else:
        print("Failed to set up sockets.")
    
def checkField(root: tk.Tk, event: tk.Event, input_ids: Dict, entry,  network:Networking) -> None:
    #fieldName: str = input_ids.get(event.widget.winfo_id())
    entry_name = entry.winfo_name()
    #print(entry_name)
    if "_equipment_id_" in entry_name:  # Check if the input ID corresponds to user ID
        equipment_id = entry.get().strip()
        networking.transmit_equipment_code(equipment_id)
    else:
       return



# --------------------------------
# WHEN CONTINUE IS CLICKED!
# --------------------------------
def on_continue_clicked(root: tk.Tk, users:Dict, input_ids, network:Networking) -> None:
    print("\n")
    users = {"red": [], "blue": []}

    if validate_equipment_ids(input_ids):
        print("Equipment IDs Checked")
    else:
        print("ruh Ro")
        resetRoot(root, users, input_ids)
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
            
            equipment_entry = build_ui_instance.get_object(input_id.replace("user_id_", "equipment_id_"))  # Get corresponding equipment field ID
            equipment_id = equipment_entry.get().strip()  # Get equipment ID
        
            if user_id and username:  # Only append if both user ID and username are not empty
                # Determine the team based on the input ID
                    team = "red" if "red" in input_id else "blue"
                    user_data.append((user_id, username, team))
                    row_num = entry.split("_")[-1] if isinstance(entry, str) else entry.winfo_name().split("_")[-1]
                    users[str(team)].append(User(int(row_num),int(equipment_id),int(user_id),str(username),str(team)))

    if not validate_users(users):
       messagebox.showerror("Warning", f"Make sure there are players on both teams prior to starting the game.")
       resetRoot(root, users, input_ids)
       return
   # Insert user data into Supabase table
    for user_id, username, team in user_data:
       # Convert user_id to int (assuming user_id should be an integer)
        try:
           user_id = int(user_id)
        except ValueError:
           messagebox.showerror("Error", "User ID must be a valid number.")
           resetRoot(root, users, input_ids)
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
    countdown.build(root, users, networking)    


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
    global build_ui_instance

    # Destroy the previous UI elements
    for child in root.winfo_children():
        child.destroy()

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
            entry_id = f"{field}{i}"
            entry = build_ui_instance.get_object(entry_id,
                                                 red_frame if "red" in field else blue_frame)
            input_ids[entry_id] = entry_id
            team = "blue" if "blue" in field else "red"
            entry.bind("<FocusOut>", lambda event, entry=entry: selectorMethod(entry, users, team, root, event, input_ids, networking))
            entry.bind ("<Return>", lambda event, entry=entry, team=team: autofill_username(entry,users,team))
    

    #root.bind("<Tab>", lambda event: checkField(root, event, input_ids, networking))
    submit_button = build_ui_instance.get_object("submit")
    root.bind("<KeyPress-F5>", lambda event: on_continue_clicked(root, users, input_ids, networking))
    submit_button.configure(command=lambda: on_continue_clicked(root, users, input_ids, networking))
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
                equipment_id_entry = entry.get().strip()
                try:
                    equipment_id = int(equipment_id_entry)
                except:
                     messagebox.showerror("Warning", f"The Equipment ID entered for {field_name} is not an number.")
                     return False
                if not equipment_id_entry:  # if equipment ID empty return false and show error
                    field_number = field_name.split("_")[-1]
                    messagebox.showerror("Warning", f"Equipment ID for {field_name} cannot be empty.")
                    return False
                else:
                    if equipment_id < 0 or equipment_id > 100 or equipment_id == 43 or equipment_id == 53:
                        messagebox.showerror("Warning", f"The Equipment ID entered for {field_name} is not valid.")
                        return False
    return True

# --------------------------------
# Checks if there are players on both teams!
# --------------------------------

def validate_users(users: Dict) -> bool:
    redInt= 0
    blueInt = 0
    
    for team in users:
        for user in users[team]:
            if "blue" in team:
                blueInt += 1
            else:
                redInt += 1

    if(blueInt < 1 or redInt < 1):
        print("Number of Players on Team Blue: " + str(blueInt))
        print("Number of Players on Team Red:" + str(redInt))
        return False
    else:
        return True
    
def resetRoot(root: tk.Tk, users: Dict, input_ids: Dict[int, str]) -> None:
    print("Reset after incorrect user entry.")
    submit_button = build_ui_instance.get_object("submit")
    root.bind("<KeyPress-F5>", lambda event: submit_button)
    submit_button.configure(state=tk.NORMAL)
    root.bind("<F12>", lambda event: clear_entry_fields(build_ui_instance))
    root.bind("<KeyPress-F5>", lambda event: on_continue_clicked(root, users, input_ids, networking))
    submit_button.configure(command=lambda: on_continue_clicked(root, users, input_ids, networking))
    
def selectorMethod(entry, users, team, root: tk.Tk, event: tk.Event, input_ids: Dict, network:Networking) -> None:
    entry_name = entry.winfo_name()
    #print(entry)
    if "_user_id_" in entry_name:
        autofill_username(entry, users, team)
    if "_equipment_id_" in entry_name:
        checkField(root, event, input_ids, entry, networking)
        

# --------------------------------
# AUTOFILL USERNAME WHEN ENTER IS CLICKED!
# --------------------------------
def autofill_username(entry, users, team):
   entry_name = entry.winfo_name()
   #print(entry)
   if "_user_id_" in entry_name:  # Check if the input ID corresponds to user ID
        user_id = entry.get().strip()
   else:
       return
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

                   # Debugging statement
                #    print("Retrieved username:", username)

                   username_entry.delete(0, tk.END)  # Clear existing content
                   username_entry.insert(0, username)

                #    ----------------
                #    PRINT STATEMENTS FOR DEBUGGING
                #    ----------------
                #    print("Username autofilled to widget number:", username_entry.winfo_id())  # Print widget number
                #    print("User team attribute:", "red" if "red" in parent_frame.winfo_name() else "blue")  # Print team attribute
                #    print("User's team set to:", team)


               else:
                   print("No username data found in response.")  # Debugging statement
           else:
               print("Username entry widget not found.")
       except Exception as e:
           print(f"An error occurred: {e}")
 
