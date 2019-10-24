import nacl.signing as nas
import nacl.encoding as nae
from nacl.exceptions import BadSignatureError
import socket
import server_coms
import time
import json

class Acteur:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.pk, self.sk = self.keyGen()
            self.socket.connect(("localhost", 12346))
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
        # print(data)
        loaded_data = json.loads(data)
        
        for key in loaded_data:
            if(key == "letters_bag"):
                self.handle_letters_bag(loaded_data[key])
            elif(key == "next_turn"):
                self.handle_next_turn(loaded_data[key])
            elif(key == "full_letterpool"):
                self.handle_full_letterpool(loaded_data[key])
            elif(key == "full_wordpool"):
                self.handle_full_wordpool(loaded_data[key])
            elif(key == "diff_letterpool"):
                self.handle_diff_letterpool(loaded_data[key])
            elif(key == "diff_wordpool"):
                self.handle_diff_wordpool(loaded_data[key])


    # ==== Override methods in subclasses to handle differently earch responses ====
    
    def handle_letters_bag(self, letters):
        pass

    def handle_next_turn(self, turn):
        pass
    
    def handle_full_letterpool(self, wordpool):
        pass

    def handle_full_wordpool(self, wordpool):
        pass

    def handle_diff_letterpool(self, diff):
        pass

    def handle_diff_wordpool(self, diff):
        pass


# actor1 = Acteur()
# print(actor1.KeyGen())

# msg = "Coucou"
# a1 = Acteur()
# pk,sk = a1.KeyGen()
# s = a1.sign(sk, msg)
# print(a1.verify(pk, msg, s))

# a = Acteur()
# server_coms.register(a.socket, "b7b597e0d64accdb6d8271328c75ad301c29829619f4865d31cc0c550046a08f")
# a.listen_server()