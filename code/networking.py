import socket
import time

from users import User
from behind_the_scenes import theGame


# Codes for transmiting (Const)
START_GAME: int = 202
END_GAME:int = 221
RED_SCORE: int = 53
BLUE_SCORE: int = 43
BUFFER: int = 1024
# time in secs
GAME_TIME: int = 380
IP: str = "127.0.0.1"
SEND_ADDRESS = ("127.0.0.1", 7500)
RECEIEVE_ADDRESS = ("127.0.0.1", 7500)
SERVER_ADDRESS: str = "0.0.0.0"
SERVER_RECEIVE_PORT: int = 7500
SERVER_TRANSMIT_PORT: int = 7501



class Networking:
    
    def __init__(self) -> None:
        pass

    def setupSockets(self) -> bool:
        try:
            # Set SO_REUSEADDR option
            self.transmitSocket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.transmitSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.receiveSocket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.receiveSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind the receive socket to the specified address and port
            self.receiveSocket.bind((SERVER_ADDRESS, SERVER_RECEIVE_PORT))
            
            # Bind the transmit socket to the specified address and port
            self.transmitSocket.bind((SERVER_ADDRESS, SERVER_TRANSMIT_PORT))
            
            return True
        except Exception as e:
            print(e)
            return False
        # try:
        #     self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #     self.transmitSocket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #     self.receiveSocket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #     self.receiveSocket.bind((SERVER_ADDRESS, SERVER_RECEIVE_PORT))
        #     self.transmitSocket.bind((SERVER_ADDRESS, SERVER_TRANSMIT_PORT))
        #     return True
        # except Exception as e:
        #     print(e)
        #     return False
    
    def close_sockets(self) -> bool:
        # Close transmit and receive sockets
        try:
            self.transmitSocket.close()
            self.receiveSocket.close()
            return True
        except Exception as e:
            print(e)
            return False
        
    def sendData(self, data: bytes, destination: tuple) -> None:
        self.transmitSocket.sendto(data, destination)

    def receiveData(self) -> bytes:
        data, address = self.receiveSocket.recvfrom(BUFFER)
        return data, address
    
    def transmit_equipment_code(self, equipment_code: str) -> bool:
        # Transmit equipment_code on port 7500 Send 
        try:
            self.transmitSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmitSocket.sendto(str.encode(str(equipment_code)), (IP,SERVER_TRANSMIT_PORT))
            return True
        except Exception as e:
            print(e)
            return False
        
    def transmit_start_game_code(self) -> bool:
        #start game
        try:
            self.transmitSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmitSocket.sendto(str.encode(str(START_GAME)), (IP, SERVER_TRANSMIT_PORT))
            return True
        except Exception as e:
            print(e)
            return False
    
    def transmit_end_game_code(self) -> bool:
    # Transmit end game code to the broadcast address
        try:
            self.transmitSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmitSocket.sendto(str.encode(str(END_GAME)), (IP, SERVER_TRANSMIT_PORT))
            return True
        except Exception as e:
            print(e)
            return False
    
    def transmit_player_hit(self, player_code: int) -> bool:
        # Transmit player hit code to the broadcast address
        try:
            self.transmitSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmitSocket.sendto(str.encode(str(player_code)), (IP, SERVER_TRANSMIT_PORT))
            return True
        except Exception as e:
            print(e)
            return False

    def run_game(self, current_game_state: theGame) -> None:
    # While the game is still running, receive data from the receive socket
        start_time: int = int(time.time())

        while int(time.time()) < (start_time + 380):
            try:
                raw_message, return_address = self.receiveSocket.recvfrom(BUFFER)
                decoded_message: str = raw_message.decode("utf-8")
                # print("Received message:", decoded_message) //DEBUGGING statement

                if decoded_message == str(START_GAME):
                    print("Start game signal received")
                else:
                    if ":" in decoded_message:
                        message_components: [str] = decoded_message.split(":")
                        if len(message_components) != 2:
                            print("Invalid message format:", decoded_message)
                            continue

                        left_code: int = int(message_components[0])
                        # print("Left code:", left_code) //DEBUGGING statement
                        right_code: int = int(message_components[1])
                        # print("Right code:", right_code) //DEBUGGING statement

                        # If player was hit instead, attribute 10 points to the attacker
                        # or if base 100points
                        if right_code == RED_SCORE:
                            current_game_state.red_base_hit(left_code)
                            self.transmit_equipment_code(str(BLUE_SCORE))
                        elif right_code == BLUE_SCORE:
                            current_game_state.blue_base_hit(left_code)
                            self.transmit_equipment_code(str(RED_SCORE))
                        elif 0 < right_code <= 100:
                            current_game_state.player_hit(left_code, right_code)
                            self.transmit_player_hit(right_code)
                        else:
                            print("Invalid codes: Left Code is " + str(left_code) + " Right Code is " + str(right_code))
                    else:
                        print("Invalid message format:", decoded_message)
            
            except Exception as e:
                continue
                # End of networking
        
        self.transmit_end_game_code()
        self.transmit_end_game_code()
        self.transmit_end_game_code()