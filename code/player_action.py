from typing import Dict
import pygubu
import tkinter as tk
import os 
import random
import threading

from behind_the_scenes import theGame
from networking import Networking
from behind_the_scenes import theGame
# from main import destroy_root
import userinterface

# If Windows, use winsound, else import playsound for music in general
if os.name == "nt":
    import winsound
else:
    import playsound

def update_timer(timer_tag: tk.Label, seconds: int, root: tk.Tk, main_frame: tk.Frame, users: Dict, network: Networking,game:theGame) -> None:
    # Update text being displayed in timer label
    mins, secs = divmod(seconds, 60)
    timer_tag.config(text=f"Time Remaining: {mins:01d}:{secs:02d}")

    # Continue counting down, destroy main frame when timer reaches 0
    if seconds > 0:
        seconds -= 1
        timer_tag.after(1000, update_timer, timer_tag, seconds, root, main_frame, users, network,game)
    else:
        main_frame.destroy()

def update_score(game: theGame,main_frame: tk.Frame, builder: pygubu.Builder,users:Dict) -> None:
    # Handle blue users
    for user in game.blue_users:
        builder.get_object(f"blue_username_{user.rownum}", main_frame).config(text=user.username)
        builder.get_object(f"blue_score_{user.rownum}", main_frame).config(text=user.game_score)
    builder.get_object("blue_total_score", main_frame).config(text=game.blue_team_score)

    # Handle red users
    for user in game.red_users:
        builder.get_object(f"red_username_{user.rownum}", main_frame).config(text=user.username)
        builder.get_object(f"red_score_{user.rownum}", main_frame).config(text=user.game_score)
    builder.get_object("red_total_score", main_frame).config(text=game.red_team_score)

    # Call every 1 second to keep updating scores and keep track of that
    main_frame.after(1000, update_score, game, main_frame, builder,users)

# Update stream Method
def update_action(game: theGame, action: tk.Frame) -> None:
    # add in scroll effect
    if len(game.game_event_actions) > 0:
        event: str = game.game_event_actions.pop()
        user_name: str =event.split("hit", 1)[0].strip()

        # create label
        event_label: tk.Label = tk.Label(action, text = event, font =("Lucida Console)", 16), bg="#0000FF") #CHECK IF COLOR IS GOOD
        event_label.pack(side = tk.TOP, fill = tk.X)

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
    game: theGame = theGame(users)

    update_score(game,main_frame, builder,users)
    update_timer(timer_tag, 360, root, main_frame, users, network,game)

