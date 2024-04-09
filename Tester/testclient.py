import socket
import errno
# Define server address and port
serverAddressPort = ("127.0.0.1", 7500)
serverRecieve = ("127.0.0.1", 7501)
bufferSize = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
print("STARTUP")

try:
    UDPClientSocket.setblocking(False)
    
    # Bind the socket to the specified address and port
    try:
        UDPClientSocket.bind(serverAddressPort)
    
    except:
        print("exit")
    
    print("Client listening on {}:{}".format(serverAddressPort[0], serverAddressPort[1]))

    while True:
        # Receive messages from the server
            try:
                msgFromServer, _ = UDPClientSocket.recvfrom(bufferSize)
                msg = "Message from Server: {}".format(msgFromServer.decode('utf-8'))
                print(msg)
            except socket.error:
                try:
                    msgToServer = input("Enter message to send to server: ")
                    UDPClientSocket.sendto(msgToServer.encode('utf-8'), serverRecieve)
                    print("Message sent to server.")
                except socket.error:
                    print("loop")
    

except KeyboardInterrupt:
    print("Client terminated by user.")

finally:
    UDPClientSocket.close()  # Close the socket when done
