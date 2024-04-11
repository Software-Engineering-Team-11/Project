from typing import Dict
import pygubu
import tkinter as tk
import os 
import random
import threading
import subprocess

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

def destroy_game(root:tk.Tk,network:Networking) -> None:

    # Close window, kill game
    network.close_sockets()
    root.destroy()

def build_new_game(root: tk.Tk) -> None:
    root.destroy()

    # Run main.py again
    subprocess.Popen(["python", "code/main.py"])

def destroy_current_game(root: tk.Tk, main_frame: tk.Frame, users: dict, network: Networking, game: theGame) -> None:
    # Destroy the main frame
    main_frame.destroy()

    # Stop playing music
    if os.name == "nt":
        winsound.PlaySound(None, winsound.SND_ASYNC)
    else:
        playsound.playsound(None, block=False)

    # Winning team display
    winner: str
    if game.blue_team_score > game.red_team_score:
        winner = "Blue Team Wins!"
    elif game.red_team_score > game.blue_team_score:
        winner = "Red Team Wins!"
    else:
        winner = "Tie Game!"
    winner_label: tk.Label = tk.Label(root, text=winner, font=("Bebas Nue", 20), bg="#FFFF00")
    winner_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Clear the user dictionary
    users["red"].clear()
    users["blue"].clear()

    # Destroy game object
    del game

    # Place restart game and end game buttons
    restart_button: tk.Button = tk.Button(root, text="Restart Game", font=("Bebas Nue", 16), bg="#FFFFFF", command=lambda: build_new_game(root))
    restart_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
    end_button: tk.Button = tk.Button(root, text="End Game", font=("Bebas Nue", 16), bg="#FFFFFF", command=lambda: destroy_game(root, network))
    end_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

def update_timer(timer_tag: tk.Label, seconds: int, root: tk.Tk, main_frame: tk.Frame, users: Dict, network: Networking,game:theGame) -> None:
    # Update text being displayed in timer label
    mins, secs = divmod(seconds, 60)
    timer_tag.config(text=f"Time Remaining: {mins:01d}:{secs:02d}")

    # Continue counting down, destroy main frame when timer reaches 0
    if seconds > 0:
        seconds -= 1
        timer_tag.after(1000, update_timer, timer_tag, seconds, root, main_frame, users, network,game)
    else:
        destroy_current_game(root, main_frame, users, network, game)

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
    # Add scroll effect to action stream with game.game_event_list queue
    if len(game.game_event_actions) > 0:
        # Get the last event from the queue along with player name
        event: str = game.game_event_actions.pop()
        player_name: str = event.split("hit", 1)[0].strip()

        # Create label for event and add to action stream
        event_label: tk.Label = tk.Label(action, text=event, font=("Fixedsys", 16), bg="#FFFFFF")
        event_label.pack(side=tk.TOP, fill=tk.X)

        # Add B to player name if they hit a base
        if "hit blue base" in event:
            for user in game.red_users:
                if user.username == player_name and "B: " not in user.username:
                    user.username = "B: " + user.username
        elif "hit red base" in event:
            for user in game.blue_users:
                if user.username == player_name and "B: " not in user.username:
                    user.username = "B: " + user.username
        
        # Remove the last event from the bottom of the action stream FIFO
        if len(action.winfo_children()) > 10:
            action.winfo_children()[0].destroy()

    # incrementally update action stream it will update every second
    action.after(1000, update_action, game, action)


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

    # start at 6:20 to match with audio
    update_timer(timer_tag, 10, root, main_frame, users, network,game)

    # 
    update_action(game,action_stream)

    game_thread: threading.Thread = threading.Thread(target=network.run_game, args=(game,), daemon=True)
    game_thread.start()
    print("Networking sockets setup:", network.setupSockets())

