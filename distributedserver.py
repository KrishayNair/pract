import socket
import threading
import json

# Shared memory dictionary
shared_memory = {}

# Lock to handle concurrent access
lock = threading.Lock()

def handle_client(conn, addr):
    global shared_memory
    print(f"New connection from {addr}")
    
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
                
            request = json.loads(data)
            action = request.get("action")
            
            if action == "read":
                key = request.get("key")
                response = shared_memory.get(key, "Key not found")
                conn.send(json.dumps(response).encode())
                
            elif action == "write":
                key = request.get("key")
                value = request.get("value")
                with lock:
                    shared_memory[key] = value
                conn.send(json.dumps({"status": "success"}).encode())
                
            elif action == "sync":
                modified_data = request.get("data")
                with lock:
                    shared_memory.update(modified_data)
                conn.send(json.dumps({"status": "updated"}).encode())
                
        except Exception as e:
            print(f"Error: {e}")
            break
    
    conn.close()
    print(f"Connection closed from {addr}")

def start_server(host="0.0.0.0", port=5000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server() 