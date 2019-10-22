import json

def register(socket, public_key):
    data = { "register" : public_key}
    print(format_to_sendable(data))
    socket.sendall(format_to_sendable(data))



def format_to_sendable(data):
    datastring = json.dumps(data)
    size = len(datastring)
    size_be_bytes = (size).to_bytes(8, byteorder="big") 
    return (size_be_bytes.decode() + datastring).encode()
