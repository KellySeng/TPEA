from acteur import Acteur
import random
import server_coms
import time
import crypto

class Auteur(Acteur):
    def __init__(self, addr, port):
        Acteur.__init__(self, addr, port)
        self.letters_bag = []
        self.current_period = 0
        self.head_block = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        self.main_loop()

    def main_loop(self):
        self.start()
        time.sleep(0.1)
        self.inject_letter(self.choose_letter(), self.current_period, self.head_block)
        server_coms.get_full_letterpool(self.socket)
        self.stop()
        #Define main  routine here

    def choose_letter(self):
        if(len(self.letters_bag) > 0):
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
        self.letters_bag = letters

    def handle_next_turn(self, turn):
        print(turn)

    def handle_full_letterpool(self, wordpool):
        print(wordpool)

    def handle_full_wordpool(self, wordpool):
        print(wordpool)

    def handle_diff_letterpool(self, diff):
        print(diff)

    def handle_diff_wordpool(self, diff):
        print(diff)


# ====
# TEST
# ====

# a = Auteur("localhost", 12346)
