import json

def register(socket, public_key):
    data = { "register" : public_key}
    socket.sendall(format_to_sendable(data))

def listen(socket):
    data = {"listen" : None}
    socket.sendall(format_to_sendable(data))

def stop_listen(socket):
    data = {"stop_listen" : None}
    socket.sendall(format_to_sendable(data))

def get_full_letterpool(socket):
    data = {"get_full_letterpool" : None}
    socket.sendall(format_to_sendable(data))

def get_letterpool_since(socket, period):
    data = {"get_letterpool_since" : period}
    socket.sendall(format_to_sendable(data))

def get_full_wordpool(socket):
    data = {"get_full_wordpool" : None}
    socket.sendall(format_to_sendable(data))

def get_wordpool_since(socket, period):
    data = {"get_wordpool_since" : period}
    socket.sendall(format_to_sendable(data))

def inject_letter(socket, letter):
    data = {"inject_letter" : letter}
    socket.sendall(format_to_sendable(data))

def inject_word(socket, word):
    data = {"inject_word" : word}
    socket.sendall(format_to_sendable(data))

def inject_raw_op(socket, buf):
    data = {"inject_raw_op" : buf}
    socket.sendall(format_to_sendable(data))

def format_to_sendable(data):
    datastring = json.dumps(data)
    size = len(datastring)
    size_be_bytes = (size).to_bytes(8, byteorder="big")
    return (size_be_bytes.decode('ISO-8859-1') + datastring).encode('ISO-8859-1').strip()
