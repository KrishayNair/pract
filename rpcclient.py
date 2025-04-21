import socket

# Create client socket and connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5000))
print("Connected to server")

# Send messages until 'Over' is entered
while True:
    msg = input("Enter message (type 'Over' to end): ")
    client.send(msg.encode())
    if msg == "Over":
        break

client.close() 