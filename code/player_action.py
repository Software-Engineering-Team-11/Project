from typing import Dict
import pygubu
import tkinter as tk
import os 
import random
import threading

from networking import Networking
# from behind_the_scenes import theGame
# from main import destroy_root
import userinterface

# If Windows, use winsound, else import playsound for music in general
if os.name == "nt":
    import winsound
else:
    import playsound

def update_timer(timer_tag: tk.Label, seconds: int, root: tk.Tk, main_frame: tk.Frame, users: Dict, network: Networking) -> None:
    # Update text being displayed in timer label
    mins, secs = divmod(seconds, 60)
    timer_tag.config(text=f"Time Remaining: {mins:01d}:{secs:02d}")

    # Continue counting down, destroy main frame when timer reaches 0
    if seconds > 0:
        seconds -= 1
        timer_tag.after(1000, update_timer, timer_tag, seconds, root, main_frame, users, network)
    else:
        main_frame.destroy()

def update_score(users:Dict,main_frame: tk.Frame, builder: pygubu.Builder) -> None:
    count_blue: int = 1
    count_red: int = 1
    for user_person in users:
        if user_person[2] == "blue":
            builder.get_object(f"{user_person[2]}_username_{count_blue}", main_frame).config(text=user_person[1])
            count_blue+=1
        if user_person[2] == "red":
            builder.get_object(f"{user_person[2]}_username_{count_red}", main_frame).config(text=user_person[1])
            count_red+=1

def build(network: Networking, users: Dict, root: tk.Tk) -> None:
    builder: pygubu.Builder = pygubu.Builder()
    try:
        builder.add_from_file("ui/player_action.ui")
    except:
        builder.add_from_file("../ui/player_action.ui")
    
    # Select random track for the game
    try:
        file = random.choice(os.listdir("assets/tracks/"))
    except:
        file = random.choice(os.listdir("../assets/tracks/"))
    
    print("TRACK PLAYING!" ,file)
    
    # Play asynchronously depending on the 
    if os.name == "nt":
        try:
            winsound.PlaySound("assets/tracks/" + file, winsound.SND_ASYNC)
        except:
            winsound.PlaySound("../assets/tracks/" + file, winsound.SND_ASYNC)
    else:
        try:
            playsound.playsound("../assets/tracks/" + file, block=False)
        except:
            playsound.playsound("assets/tracks/" + file, block=False)
    
    # Place everything on the center of the window
    main_frame: tk.Frame = builder.get_object("master", root)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    timer_tag: tk.Label = builder.get_object("countdown_label", main_frame)

    # get where the action happens (middle frame)
    action_stream: tk.Frame = builder.get_object("action_stream_frame", main_frame)
    action_stream.pack_propagate(False)

    # Create game :
    # game: GameState = GameState(users)

    update_score(users,main_frame, builder)
    update_timer(timer_tag, 360, root, main_frame, users, network)
