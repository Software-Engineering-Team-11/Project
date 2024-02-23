import socket
import time


# Codes for transmiting (Const)
START_GAME: int = 202
END_GAME:int = 221
RED_SCORE: int = 53
BLUE_SCORE: int = 43
BUFFER: int = 1024
# time in secs
GAME_TIME: int = 360
IP: str = "127.0.0.1"
SERVER_ADDRESS: str = "0.0.0.0"
SERVER_PORT: int = 7500



class Networking:
    def __init__(self) -> None:
        pass

    def setupSockets(self) -> bool:
        # Set up sockets
        try:
            self.transmitSocket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.receiveSocket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.receiveSocket.bind((SERVER_ADDRESS, SERVER_PORT))
            return True
        except Exception as e:
            print(e)
            return False