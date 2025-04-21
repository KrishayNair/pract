from xmlrpc.client import ServerProxy

# Connect to server
server = ServerProxy('http://localhost:8000')
print("Connected to RMI Server")

# Call remote methods
while True:
    print("\n1. Add numbers")
    print("2. Multiply numbers")
    print("3. Exit")
    choice = input("Enter choice (1-3): ")
    
    if choice == '3':
        break
        
    a = int(input("Enter first number: "))
    b = int(input("Enter second number: "))
    
    if choice == '1':
        result = server.add(a, b)
        print(f"Sum: {result}")
    elif choice == '2':
        result = server.multiply(a, b)
        print(f"Product: {result}")

print("Client closed") 