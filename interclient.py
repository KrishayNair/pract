import socket

# Create TCP client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to server on localhost port 5000
client.connect(('localhost', 5000))
print("Connected!")

# Keep sending numbers until 'stop' is entered
while True:
    num = input("Enter number (or 'stop' to end): ")
    # Send number to server
    client.send(num.encode())
    if num == "stop":
        break

# Receive and print the sum from server
result = client.recv(1024).decode()
print("Sum of numbers:", result)
# Close connection
client.close() 