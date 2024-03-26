import socket

# Define server address and port
serverAddressPort = ("127.0.0.1", 7500)
bufferSize = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
print("STARTUP")
try:
    # Bind the socket to the specified address and port
    UDPClientSocket.bind(serverAddressPort)

    print("Client listening on {}:{}".format(serverAddressPort[0], serverAddressPort[1]))

    while True:
        # Receive messages from the server
        msgFromServer, _ = UDPClientSocket.recvfrom(bufferSize)
        msg = "Message from Server: {}".format(msgFromServer.decode('utf-8'))
        print(msg)

except KeyboardInterrupt:
    print("Client terminated by user.")

finally:
    UDPClientSocket.close()  # Close the socket when done
