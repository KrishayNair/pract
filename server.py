import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5000))
server.listen(1)
print("Waiting for connection...")
client, addr = server.accept()
print("Connected!")

sum = 0
while True:
    data = client.recv(1024).decode()
    if data == "stop":
        break
    sum += int(data)

client.send(str(sum).encode())
client.close()
server.close() 