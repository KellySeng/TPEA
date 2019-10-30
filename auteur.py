import random
import time
import threading

from acteur import Acteur
import server_coms
import crypto

class Auteur(Acteur):
    def __init__(self, addr, port):
        Acteur.__init__(self, addr, port)
        self.letters_bag = []
        self.current_period = 0
        self.letter_injected_this_turn = False
        self.head_block = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        self.cond = threading.Condition()
        self.main_loop()


    def main_loop(self):
        self.start()
        time.sleep(0.1) # TODO Find a way to improve this (Wait for the server to respond to register and send the letter bag)
        while True:
            self.cond.acquire()
            if(not self.letter_injected_this_turn):
                self.letter_injected_this_turn = True
                choosen_letter = self.choose_letter()
                self.letters_bag.remove(choosen_letter)
                self.inject_letter(choosen_letter, self.current_period, self.head_block)
                server_coms.get_full_letterpool(self.socket)
            try:
                self.cond.wait()
            except KeyboardInterrupt:
                break
            finally:
                self.cond.release()
            
        self.stop()
        #Define main  routine here

    def choose_letter(self):
        if(self.letters_bag):
            return random.choice(self.letters_bag)
        else:
            return None

    def inject_letter(self, letter, period, head):

        if(len(letter) == 1):
            to_inject = {
                "letter" : letter,
                "period" : period,
                "head" : head,
                "author" : self.pkstr,
                "signature" : crypto.sign_letter(self.sk,letter,period,head,self.pkstr)
            }
            print(to_inject)
            server_coms.inject_letter(self.socket, to_inject)

    # TODO ==== Define how to handle server responses in this class here ====
    # TODO Pay attention to criticals sections

    def handle_letters_bag(self, letters):
        self.cond.acquire()
        self.letters_bag = letters
        self.cond.release()

    def handle_next_turn(self, turn):
        self.cond.acquire()
        self.current_period = turn
        self.letter_injected_this_turn = False
        self.cond.notify_all()
        self.cond.release()

    def handle_full_letterpool(self, letterpool):
        self.current_letterpool = letterpool["letters"]

    def handle_full_wordpool(self, wordpool):
        self.current_wordpool = wordpool["words"]

    def handle_diff_letterpool(self, diff):
        # TODO Define
        print(diff)

    def handle_diff_wordpool(self, diff):
        # TODO Define
        print(diff)


# ====
# TEST
# ====

a = Auteur("localhost", 12346)
