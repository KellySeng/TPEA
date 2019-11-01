import random
from acteur import Acteur
import server_coms
import crypto

class Auteur(Acteur):

    def __init__(self, addr, port):
        Acteur.__init__(self, addr, port)
        self.letters_bag = []
        self.letter_injected_this_turn = False
        self.main_loop()

    def start(self):
        Acteur.start(self)
        # Need to register and set the current period
        server_coms.register(self.socket, self.pkstr)
        self.cond.acquire()
        while(self.letters_bag == []):
            try:
                self.cond.wait()
            except KeyboardInterrupt:
                self.cond.release()
                self.stop()
                exit(0)
        self.cond.release()

    def main_loop(self):
        self.start()
        while self.letters_bag:
            self.cond.acquire()
            if(not self.letter_injected_this_turn):
                self.letter_injected_this_turn = True
                choosen_letter = self.choose_letter()
                self.inject_letter(choosen_letter, self.current_period, self.head_block)
            try:
                self.cond.wait()
            except KeyboardInterrupt:
                break
            finally:
                self.cond.release()

        self.stop()

    def choose_letter(self):
        if(self.letters_bag):
            res = random.choice(self.letters_bag)
            self.letters_bag.remove(res)
            return res
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
            # print(to_inject)
            server_coms.inject_letter(self.socket, to_inject)

    # TODO ==== Define how to handle server responses in this class here ====
    # TODO Pay attention to criticals sections

    def handle_letters_bag(self, letters):
        self.cond.acquire()
        self.letters_bag = letters
        self.cond.notify_all()
        self.cond.release()

    def handle_next_turn(self, turn):
        self.cond.acquire()
        self.current_period = turn
        self.letter_injected_this_turn = False
        self.cond.notify_all()
        self.cond.release()

    def handle_diff_letterpool(self, diff):
        # TODO Define
        print(diff)

    def handle_diff_wordpool(self, diff):
        # TODO Define
        print(diff)

    def handle_inject_letter(self, letter):
        # TODO Define
        pass

    def handle_inject_word(self, word):
        # TODO Define
        pass

    def handle_inject_raw_op(self, raw_op):
        # TODO Define
        pass


# ====
# TEST
# ====

a = Auteur("localhost", 12346)
