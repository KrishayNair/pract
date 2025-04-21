import socket
import time
import threading

# Server configuration
HOST = 'localhost'
PORT = 5000
sequence_number = 0

def handle_client(client_socket):
    global sequence_number
    try:
        while True:
            # Create and send message
            message = f"Message {sequence_number}"
            print(f"Server sending: {message}")
            client_socket.send(message.encode())
            sequence_number += 1
            time.sleep(2)  # Wait 2 seconds between messages
    except:
        print("Client disconnected")
    finally:
        client_socket.close()

# Create server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"Server listening on {HOST}:{PORT}")

# Accept connections
while True:
    client_socket, addr = server.accept()
    print("Client connected")
    # Start new thread for each client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start() 