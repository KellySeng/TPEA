import nacl.signing as nas
import nacl.encoding as nae
from nacl.exceptions import BadSignatureError
import socket
import server_coms

class Acteur:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(("localhost", 12346))
        except ConnectionRefusedError:
            print("Connection to server failed")


    def KeyGen(self, length=1024):
        sk = nas.SigningKey.generate()
        pk = sk.verify_key
            
        return pk, sk

    def sign(self, sk, data):
        return sk.sign(data.encode()).signature

    def verify(self, pk, data, signature):
        try:
            pk.verify(data.encode(), signature)
            return True
        except (BadSignatureError):
            return False
        
# actor1 = Acteur()
# print(actor1.KeyGen())

# msg = "Coucou"
# a1 = Acteur()
# pk,sk = a1.KeyGen()
# s = a1.sign(sk, msg)
# print(a1.verify(pk, msg, s))

a = Acteur()
server_coms.register(a.socket, "Test")
