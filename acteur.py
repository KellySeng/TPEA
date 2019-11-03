import socket
import json
import threading
import crypto
import server_coms
import blockchain
from dictionary import Dictionary

class Acteur:

    def __init__(self,addr,port,namefile):
        self.addr = addr
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pk, self.sk = crypto.keyGen()
        self.pkstr = crypto.pkstr_of_pk(self.pk)
        self.listener = Listener(self)
        self.cond = threading.Condition()

        self.current_period = -1
        self.trwordpool = {}
        self.wordpool = [] # store injected words when trwordpool not initialized yet
        self.head = ""

        self.dico = Dictionary()
        self.namefile = namefile

        # Max number of time we try get a better head block before giving up
        # One reason may be that we can't create another block
        self.max_ite = 50
        # timeout when waiting for a new word injected
        self.timeout = 0.1

    def start(self):
        try:
            self.socket.connect((self.addr,self.port))
        except ConnectionRefusedError:
            print("Connection to server failed")
            exit(0)
        self.dico.load_file(self.namefile)
        self.listener.start()
        server_coms.listen(self.socket)

        # Get period and wordpool
        server_coms.get_full_wordpool(self.socket)
        self.cond.acquire()
        while not self.trwordpool:
            try:
                self.cond.wait()
            except KeyboardInterrupt:
                self.cond.release()
                self.stop()
                exit(0)
        self.cond.release()

    def stop(self):
        self.listener.stop_listener()
        self.listener.join()

    # ==== Override methods in subclasses to handle differently earch responses ====

    def handle_full_wordpool(self, wordpool):
        """
        Only used at the beginning of an Acteur in order to get the period and
        create the trwordpool
        """
        self.cond.acquire()
        if self.current_period < wordpool["current_period"]:
            self.current_period = wordpool["current_period"]
        self.trwordpool = blockchain.wordpool_to_trwordpool(self.dico,wordpool)
        for block in self.wordpool:
            blockchain.add_block(self.dico,self.trwordpool,block)
        self.wordpool = []
        self.cond.notify_all()
        self.cond.release()

    def end(self):
        scores_politicians, scores_authors = blockchain.total_scores(self.dico,self.trwordpool)
        to_print = "=====================================================================\n"
        to_print += "SCORES POLITICIANS\n\n"
        for h,s in scores_politicians.items():
            to_print += h + " : " + str(s) + "\n"

        to_print += "\nSCORES AUTHORS\n\n"
        for h,s in scores_authors.items():
            to_print += h + " : " + str(s) + "\n"

        to_print += "=====================================================================\n"
        print(to_print)

    def handle_inject_word(self, word):
        pass

    def handle_letters_bag(self, letters):
        pass

    def handle_next_turn(self, turn):
        pass

    def handle_full_letterpool(self, letterpool):
        pass

    def handle_diff_letterpool(self, diff):
        pass

    def handle_diff_wordpool(self, diff):
        pass

    def handle_inject_letter(self, letter):
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
                if not msg:
                    continue
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

# a = Acteur("localhost",12346, "dict/dict_100000_1_10.txt")
# a.start()
