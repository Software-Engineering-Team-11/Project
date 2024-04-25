# Team 11
This project was developed as part of the Fall 2024 semester of the Software Engineering course at the University of Arkansas. The goal of the project was to recreate the Photon laser tag system using more up to date technologies.

## DOWNLOAD THE PROJECT
You can obtain the project either by downloading it as a ZIP file or by cloning the repository to your local machine. To clone the repository, use the following command:
```
git clone https://github.com/Software-Engineering-Team-11/Project.git
```

After you have cloned the repository open the project in the terminal
```
cd Project
```
***If you have already downloaded the project please delete the folder and redownload it***

## NEEDED DOWNLOADS

***Step 1: Install pip***

For non-windows users:
1. Open a terminal
2. Install pip for python3 by typing and entering this command:
```
sudo apt install python3-pip
```
3. If pip does not work use:
```
sudo apt install Python-
```

For windows users:
1. Open a terminal
2. Install pip for python by typing and entering this command:
```
python -m pip install --upgrade pip
```

***Step 2: Install packages***

Non-windows users:
1. In the terminal type and enter each of the following commands one by one:
```
pip install python-dotenv
pip install supabase-py
pip install supabase
pip install pygubu
pip install pillow
pip install opencv-python
pip install playsound
sudo apt install python3-tk
sudo apt install python3-pil.imagetk
```
2. Each command will download and install a different package needed to run the project. Once you have downloaded all of the packages you are ready to continue.


Windows users:
1. In the terminal type and enter each of the following commands one by one:
```
pip install python-dotenv
pip install tk
pip install supabase-py
pip install pygubu
pip install pillow
pip install opencv-python
```
2. Each command will download and install a different package needed to run the project. Once you have downloaded all of the packages you are ready to continue.

***If if pip install does not work, replace pip install before the command with:***
```
sudo apt install python3-"(package name)"
```


## Run Traffic Generator
To start, open two different terminals; you'll need both. One will run the traffic generator, and the other will run the main code.

For non-Windows users, use:
```
python3 code/trafficgenerator.py
```
For Windows users, use:
```
python code/trafficgenerator.py
```
After running this command, you'll be prompted to enter four equipment IDs. We recommend using IDs 1, 2, 3, and 4. You can use different IDs, but they all must be unique, between the numbers 1 - 30, and cannot be duplicated. Once you've entered the IDs, you'll see a message that says "Waiting for start from game_software." When you see this, switch to your second terminal.

## Run the Game Software
After running the traffic generator software open your other terminal to run the main code.

1. Navigate to the project directory:
```
cd Project
```
2. Run the main code:

For non-Windows users, use:
```
python3 code/main.py
```
For Windows users, use:
```
python code/main.py
```

After using this command, the player entry screen will pop up. Fill in the equipment id field using the same four ids used for the traffic generator, assigning two to the blue team and two to the red team. Then fill in the user id field, again we recommended used ids 1, 2, 3, and 4. You can use different IDs, but they all must be unique, between the numbers 1 - 30, and cannot be duplicated. Once you insert the ID, press the "Enter" key. This action will auto-populate the username if the player is in Supabase. If the user does not exist with that id, input their name in the Username field and they will be added to Supabase for future reference. Next, click "Continue" to bring you to the countdown screen and start the game.


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
