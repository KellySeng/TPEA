import nacl.signing as nas
import nacl.encoding as nae
from nacl.exceptions import BadSignatureError
import socket
import server_coms
import time
import json

class Acteur:

    def __init__(self,addr,port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.pk, self.sk = self.keyGen()
            self.key_str = self.pk.to_curve25519_public_key()._public_key.hex()
            self.socket.connect((addr,port))
        except ConnectionRefusedError:
            print("Connection to server failed")

    def keyGen(self, length=1024):
        sk = nas.SigningKey.generate()
        pk = sk.verify_key
        return pk, sk

    def sign(self,data):
        return self.sk.sign(data.encode()).signature

    def verify(self,pk,data, signature):
        try:
            pk.verify(data.encode(), signature)
            return True
        except (BadSignatureError):
            return False

    def listen_server(self):
        time.sleep(1)
        try:
            msg_length_b = self.socket.recv(8, socket.MSG_DONTWAIT)
            msg_length = int.from_bytes(msg_length_b, "big")
            data = self.socket.recv(msg_length, socket.MSG_DONTWAIT).decode("utf-8", "ignore") # TODO Stop ignoring most ASCII characters. But why is it random since dict use only letters ?

        except BlockingIOError: # Nothing to read
            return
        print(data)
        loaded_data = json.loads(data)
        
        # TODO Define all methods to handle responses
        for key in loaded_data:
            if(key == "letters_bag"):
                pass
            elif(key == "next_turn"):
                pass
            elif(key == "full_letterpool"):
                pass
            elif(key == "full_wordpool"):
                pass
            elif(key == "diff_letterpool"):
                pass
            elif(key == "diff_wordpool"):
                pass

        
# actor1 = Acteur()
# print(actor1.KeyGen())

# msg = "Coucou"
# a1 = Acteur()
# pk,sk = a1.KeyGen()
# s = a1.sign(sk, msg)
# print(a1.verify(pk, msg, s))

a = Acteur("localhost",12346)
server_coms.register(a.socket, a.key_str)
print(a.key_str)
a.listen_server()
