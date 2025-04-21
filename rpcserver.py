import socket

# Create server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5000))
server.listen(1)
print("Server started\nWaiting for client...")

# Accept client connection
client, addr = server.accept()
print("Client connected")

# Receive messages until 'Over' is received
while True:
    msg = client.recv(1024).decode()
    if msg == "Over":
        break
    print("Received:", msg)

print("Closing connection")
client.close()
server.close() 