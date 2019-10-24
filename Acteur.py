import socket
import server_coms
import time
import json
import crypto

class Acteur:

    def __init__(self,addr,port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.pk, self.sk = crypto.keyGen()
            self.socket.connect((addr,port))
        except ConnectionRefusedError:
            print("Connection to server failed")

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

# msg = "Coucou"
# a1 = Acteur("localhost",12346)
# sig = crypto.sign(a1.sk, msg)
# print(sig)
# print(crypto.verify(crypto.pkstr_of_pk(a1.pk),msg,sig))


a = Acteur("localhost",12346)
server_coms.register(a.socket, crypto.pkstr_of_pk(a.pk))
a.listen_server()
