import socket
import json

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

def send_request(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_IP, SERVER_PORT))
        client.send(json.dumps(request).encode())
        response = client.recv(1024).decode()
        return json.loads(response)

def read_memory(key):
    response = send_request({"action": "read", "key": key})
    print(f"Read from memory [{key}]: {response}")

def write_memory(key, value):
    response = send_request({"action": "write", "key": key, "value": value})
    print(f"Write to memory [{key}]: {response}")

def sync_memory(changes):
    response = send_request({"action": "sync", "data": changes})
    print(f"Memory synced: {response}")

def main():
    node_id = input("Enter node ID: ")
    
    while True:
        print("\n1. Read Memory")
        print("2. Write Memory")
        print("3. Sync Changes")
        print("4. Exit")
        
        choice = input("Choose an action: ")
        
        if choice == "1":
            key = input("Enter key to read: ")
            read_memory(key)
            
        elif choice == "2":
            key = input("Enter key to write: ")
            value = input("Enter value: ")
            write_memory(key, value)
            
        elif choice == "3":
            changes = {}
            while True:
                key = input("Enter key to modify (or 'done' to finish): ")
                if key == "done":
                    break
                value = input(f"Enter new value for {key}: ")
                changes[key] = value
            
            sync_memory(changes)
            
        elif choice == "4":
            print("Exiting client.")
            break
            
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main() 