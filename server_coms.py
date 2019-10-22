import json

def register(socket, public_key):
    data = { "register" : public_key}
    print(format_to_sendable(data))
    socket.sendall(format_to_sendable(data))



def format_to_sendable(data):
    datastring = json.dumps(data)
    size = len(datastring)
    size_be_hex = (size).to_bytes(8, byteorder="little").hex() # TODO Envoyer un hex ici pour la taille ??
    # size_be_bin = bin(size)[2:].zfill(64)
    # print(size_be_hex+datastring)
    return (str(size) + datastring).encode()


# register(None, "Saluteeeee")