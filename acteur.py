import socket
import json
import threading

import server_coms
import crypto

class Acteur:

    def __init__(self,addr,port):
        self.addr = addr
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pk, self.sk = crypto.keyGen()
        self.pkstr = crypto.pkstr_of_pk(self.pk)
        self.listener = Listener(self)
        self.cond = threading.Condition()
        
        self.head_block = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        self.current_period = 0
        self.current_letterpool = []
        self.current_wordpool = []

    def start(self):
        try:
            self.socket.connect((self.addr,self.port))
        except ConnectionRefusedError:
            print("Connection to server failed")
        self.listener.start()

    def stop(self):
        self.listener.stop_listener()
        self.listener.join()

    # ==== Override methods in subclasses to handle differently earch responses ====

    def handle_letters_bag(self, letters):
        pass

    def handle_next_turn(self, turn):
        pass

    def handle_full_letterpool(self, letterpool):
        pass

    def handle_full_wordpool(self, wordpool):
        pass

    def handle_diff_letterpool(self, diff):
        pass

    def handle_diff_wordpool(self, diff):
        pass

    def handle_inject_letter(self, letter):
        pass
    
    def handle_inject_word(self, word):
        pass
    
    def handle_inject_raw_op(self, raw_op):
        pass

# Class for a thread that will listen to all messages from the central server
class Listener(threading.Thread):

    def __init__(self,acteur):
        threading.Thread.__init__(self)
        self.acteur = acteur
        self.running = True
        self.acteur.socket.settimeout(1.0) # Use a timeout to be able to close the socket properly

    def run(self):
        while self.running:
            try:
                # Reading the length of the message
                msg_length_b = self.acteur.socket.recv(8)
                msg_length = int.from_bytes(msg_length_b, "big")
                # Reading the message
                msg = self.acteur.socket.recv(msg_length).decode("utf-8", "ignore")
            except socket.timeout:
                continue

            # Convert json to python dictionary
            loaded_msg = json.loads(msg)
            # Match
            for key in loaded_msg:
                if(key == "letters_bag"):
                    self.acteur.handle_letters_bag(loaded_msg[key])
                elif(key == "next_turn"):
                    self.acteur.handle_next_turn(loaded_msg[key])
                elif(key == "full_letterpool"):
                    self.acteur.handle_full_letterpool(loaded_msg[key])
                elif(key == "full_wordpool"):
                    self.acteur.handle_full_wordpool(loaded_msg[key])
                elif(key == "diff_letterpool"):
                    self.acteur.handle_diff_letterpool(loaded_msg[key])
                elif(key == "diff_wordpool"):
                    self.acteur.handle_diff_wordpool(loaded_msg[key])
                elif(key == "inject_letter"):
                    self.acteur.handle_inject_letter(loaded_msg[key])
                elif(key == "inject_word"):
                    self.acteur.handle_inject_word(loaded_msg[key])
                elif(key == "inject_raw_op"):
                    self.acteur.handle_inject_raw_op(loaded_msg[key])                    
        self.acteur.socket.close() # Closes the socket once the thread has stopped running properly

    def stop_listener(self):
        self.running = False


# ====
# Test
# ====

# a = Acteur("localhost",12346)
# a.start()
