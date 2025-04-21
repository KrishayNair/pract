import socket

# Client configuration
HOST = 'localhost'
PORT = 5000

class Message:
    def __init__(self, sequence_number, message):
        self.sequence_number = sequence_number
        self.message = message

# List to store received messages
received_messages = []

try:
    # Create client socket and connect
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("Connected to server")

    # Receive messages
    while True:
        data = client.recv(1024).decode()
        if not data:
            break
            
        print(f"Receiver received: {data}")
        
        # Extract sequence number and store message
        parts = data.split()
        sequence_number = int(parts[1])
        received_messages.append(Message(sequence_number, data))
        
        # Sort messages by sequence number
        received_messages.sort(key=lambda x: x.sequence_number)
        
        # Print ordered messages
        print("Ordered messages:")
        for msg in received_messages:
            print(msg.message)

except Exception as e:
    print("Disconnected from server")
finally:
    client.close() 