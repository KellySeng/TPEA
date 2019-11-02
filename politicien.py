import random
from acteur import Acteur
import server_coms
import crypto
import blockchain
import letterpool

class Politicien(Acteur):
    def __init__(self, addr, port, namefile):
        Acteur.__init__(self, addr, port, namefile)
        self.trletterpool = {}
        self.letterpool = [] # store injected letters when trletterpool not initialized yet
        self.main_loop()

    def start(self):
        Acteur.start(self)
        server_coms.get_full_letterpool(self.socket)
        self.cond.acquire()
        while not self.trletterpool:
            try:
                self.cond.wait()
            except KeyboardInterrupt:
                self.cond.release()
                self.stop()
                exit(0)
        self.cond.release()

    def main_loop(self):
        self.start()
        while True:
            self.cond.acquire()
            head = blockchain.get_best_head(self.dico,self.trwordpool)
            self.cond.release()
            word = self.choose_word(head)
            self.inject_word(word, head)
        self.stop()

    def choose_word(self,head):
        # TODO VERY random and won't stop until it finds a match, even if it's impossible (but will take into account letters that are added while searching for a word)

        # TODO Stop once this period is over even if nothing was found, to focus on the next one

        current_word_str = ""
        current_word = []
        authors_in_current_word = set()

        while not self.dico.is_word(current_word_str):
            if(self.dico.exists_word_with_prefix(current_word_str)):
                next_letter = self.choose_letter(head,authors_in_current_word)
                if next_letter is None:
                    # Cannot create a word big enough to fit with this prefix
                    current_word_str = ""
                    current_word = []
                    authors_in_current_word.clear()
                    continue
                current_word_str += next_letter["letter"]
                current_word.append(next_letter)
                authors_in_current_word.add(next_letter["author"])
            else:
                current_word_str = ""
                current_word = []
                authors_in_current_word.clear()
        return current_word

    def choose_letter(self,head,exclude_authors={}):
        letters = []
        self.cond.acquire()
        for l in self.trletterpool[head]["letters"]:
            if not l["author"] in exclude_authors:
                letters.append(l)
        self.cond.release()

        if letters:
            return random.choice(letters)
        return None

    def inject_word(self, word, head):
        to_inject = {
            "word" : word,
            "head" : head,
            "politician" : self.pkstr,
            "signature" : crypto.sign_word(self.sk, word, head, self.pkstr)
        }
        print(to_inject)
        server_coms.inject_word(self.socket, to_inject)

    # TODO ==== Define how to handle server responses in this class here ====

    def handle_full_letterpool(self, pool):
        self.cond.acquire()
        self.trletterpool = letterpool.letterpool_to_trletterpool(pool)
        for letter in self.letterpool:
            letterpool.add_letter(self.trletterpool,letter)
        self.letterpool = []
        self.cond.notify_all()
        self.cond.release()

    def handle_next_turn(self, turn):
        self.cond.acquire()
        self.current_period = turn
        self.cond.notify_all()
        self.cond.release()

    def handle_diff_letterpool(self, diff):
        # TODO Define
        print(diff)

    def handle_diff_wordpool(self, diff):
        # TODO Define
        print(diff)

    def handle_inject_letter(self, letter):
        self.cond.acquire()
        if self.trletterpool:
            letterpool.add_letter(self.trletterpool,letter)
        else:
            self.letterpool.append(letter)
        self.cond.release()

    def handle_inject_raw_op(self, raw_op):
        # TODO Define
        pass


p = Politicien("localhost", 12346, "dict/dict_100000_1_10.txt")
