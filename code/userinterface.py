import tkinter as tk
import pygubu
from tkinter import messagebox
from typing import Dict, List
from supabase_manager import supabase

def on_continue_clicked(root:tk.Tk,users, input_ids) -> None:
    #  if len(users["blue"]) < 1 or len(users["red"]) < 1:
    #     messagebox.showerror("Error", "There must be at least 1 user on each team")
        print("HEY!")
        return

def builder(root:tk.Tk, users :dict) -> None:
    builder: pygubu.Builder = pygubu.Builder()
    builder.add_from_file("ui/player_interface.ui")

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

    # data = supabase.table("users").select("*").execute()
    # print(data)
    
