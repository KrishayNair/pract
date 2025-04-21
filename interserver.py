import socket

# Create TCP server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind to localhost on port 5000
server.bind(('localhost', 5000))
# Listen for incoming connections
server.listen(1)
print("Waiting for connection...")
# Accept client connection
client, addr = server.accept()
print("Connected!")

# Initialize sum variable
sum = 0
# Keep receiving numbers until 'stop' is received
while True:
    data = client.recv(1024).decode()
    if data == "stop":
        break
    # Add received number to sum
    sum += int(data)

# Send final sum back to client
client.send(str(sum).encode())
# Close connections
client.close()
server.close() 