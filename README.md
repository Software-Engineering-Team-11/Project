# Team 11
This project is still being developed as part of the Fall 2024 semester of the Software Engineering course at the University of Arkansas. The goal of this project is to recreate the Photon laser tag system using more up to date technologies.

## DOWNLOAD THE PROJECT
You can obtain the project either by downloading it as a ZIP file or by cloning the repository to your local machine. To clone the repository, use the following command:
```
git clone https://github.com/Software-Engineering-Team-11/Project.git
```

After you have cloned the repository open the project in the terminal
```
cd Project
```

## NEEDED DOWNLOADS

*** Ensure all previous versions of the following are uninstalled if you have installed them for prior projects. ***

In order for this project to run you will need to download the following:

First make sure you have pip installed, you can use this command to install it:
```
sudo apt install python3-pip
```

If pip does not work use:
```
sudo apt install Python-
```

Non-windows users install these packages:
```
pip install python-dotenv
pip install tk
pip install supabase-py
pip install supabase
pip install pygubu
pip install pillow
pip install opencv-python
pip install pil.imagetk
pip install playsound
```
Windows users install these packages:
```
pip install python-dotenv
pip install tk
pip install supabase-py
pip install pygubu
pip install pillow
pip install opencv-python
```
## Run Traffic Generator
To start, open two different terminals; you'll need both. One will run the traffic generator, and the other will run the main code.

For non-Windows users, use:
```
python3 code/TrafficGenerator.py
```
For Windows users, use:
```
python code/TrafficGenerator.py
```
After running this command, you'll be prompted to enter four equipment IDs. We recommend using IDs 1, 2, 3, and 4. You can use different IDs, but they all must be unique and cannot be duplicated. Once you've entered the IDs, you'll see a message that says "Waiting for start from game_software." When you see this, switch to your second terminal.

## Run the Game Software
After running the test software open another terminal to run the main code.

For non-Windows users, use:
```
python3 code\main.py
```
For Windows users, use:
```
python code\main.py
```

After using this command, the player entry screen will pop up. Fill in the equipment id field using the same four ids used for the traffic generator, assigning two to the blue team and two to the red team. Then fill in the user id field, again we reccomened used ids 1, 2, 3, and 4. Once you insert the ID, press the "Enter" key. This action will auto-populate the username if the player is in Supabase. If the user does not exist with that id, input their name in the Username field and they will be added to Supabase for future reference. Next, click "Continue" to bring you to the countdown screen.


## TEAM MEMBERS
```
Cali Brewer - crb054 
Kristen Babbitt - KristenBabbitt 
Rafael Balassiano - Rafaelbala223 
Rafael Rasse - rafaelrasse 
Logan Deloach - LoganDeLoach 
Chase Hudak - ChaseLHudak 
Ben Keller - Keller2
```
