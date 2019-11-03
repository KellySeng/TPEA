import random
from acteur import Acteur
import server_coms
import crypto
import blockchain

class Auteur(Acteur):

    def __init__(self, addr, port, namefile):
        Acteur.__init__(self, addr, port, namefile)
        self.letters_bag = []
        self.main_loop()

    def start(self):
        Acteur.start(self)
        # Register
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
        ite = 0
        while self.letters_bag and ite < self.max_ite:
            self.cond.acquire()

            # Test if we get a better head than last iteration
            best_head = blockchain.get_best_head(self.dico, self.trwordpool)
            if best_head == self.head:
                try:
                    self.cond.wait(self.timeout)
                    ite += 1
                    continue
                except KeyboardInterrupt:
                    break
                finally:
                    self.cond.release()

            # We found a new head block
            else:
                ite = 0
                self.head = best_head
                choosen_letter = self.choose_letter()
                self.inject_letter(choosen_letter, self.current_period, best_head)
                try:
                    self.cond.wait(self.timeout)
                except KeyboardInterrupt:
                    break
                finally:
                    self.cond.release()

        # The loop may have been stopped because there are no more letters
        # in the letters bag. We want to stop only if there is no more activities in
        # the blockchain
        while ite < self.max_ite:
            self.cond.acquire()
            best_head = blockchain.get_best_head(self.dico, self.trwordpool)
            if best_head == self.head:
                ite += 1
            else:
                ite = 0
                self.head = best_head
            try:
                self.cond.wait(self.timeout)
            except KeyboardInterrupt:
                break
            finally:
                self.cond.release()

        self.end()
        self.stop()

    def choose_letter(self):
        res = random.choice(self.letters_bag)
        self.letters_bag.remove(res)
        return res

    def inject_letter(self, letter, period, head):
        if(len(letter) == 1):
            to_inject = {
                "letter" : letter,
                "period" : period,
                "head" : head,
                "author" : self.pkstr,
                "signature" : crypto.sign_letter(self.sk,letter,period,head,self.pkstr)
            }
            server_coms.inject_letter(self.socket, to_inject)

    # TODO ==== Define how to handle server responses in this class here ====

    def handle_letters_bag(self, letters):
        self.cond.acquire()
        self.letters_bag = letters
        self.cond.notify_all()
        self.cond.release()

    # Maybe useless since we don't use turns
    def handle_next_turn(self, turn):
        self.cond.acquire()
        self.current_period = turn
        self.cond.release()

    def handle_inject_word(self, word):
        self.cond.acquire()
        if self.trwordpool:
            blockchain.add_block(self.dico,self.trwordpool,word)
            self.cond.notify_all()
        else:
            self.wordpool.append(word)
        self.cond.release()

    def handle_inject_raw_op(self, raw_op):
        pass


# ====
# TEST
# ====

# a = Auteur("localhost", 12346, "dict/dict_100000_1_10.txt")
