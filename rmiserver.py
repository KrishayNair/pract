from xmlrpc.server import SimpleXMLRPCServer

# Create server
server = SimpleXMLRPCServer(('localhost', 8000))
print("RMI Server started on port 8000")

# Define remote methods
def add_numbers(a, b):
    return a + b

def multiply_numbers(a, b):
    return a * b

# Register methods
server.register_function(add_numbers, 'add')
server.register_function(multiply_numbers, 'multiply')

# Start server
server.serve_forever() 