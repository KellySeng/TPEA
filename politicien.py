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
        ite = 0
        while ite < self.max_ite:
            self.cond.acquire()

            best_head = blockchain.get_best_head(self.dico,self.trwordpool)
            if best_head != self.head:
                # There are words still injected, we can continue trying building blocks
                ite = 0
                self.head = best_head
            else:
                # No new best block for a while, maybe we can't create anymore
                ite += 1

            # We release the lock in order to take into account new letters during the search
            self.cond.release()
            found,word = self.choose_word(best_head)
            self.cond.acquire()

            if found:
                self.inject_word(word,best_head)

            # A break in order to prepare for next iteration (new letters for exemple)
            try:
                self.cond.wait(self.timeout)
            except KeyboardInterrupt:
                break
            finally:
                self.cond.release()

        self.end()
        self.stop()

    def choose_word(self,head):
        """
        VERY random and won't stop until it finds a match or when the number
        of iterations is too high
        """
        if not (head in self.trletterpool):
            return False, []
        if not self.trletterpool[head]["letters"]:
            return False, []

        current_word_str = ""
        current_word = []
        authors_in_current_word = set()
        dico_tmp = self.dico.dico

        ite = 0
        max_ite = 10000 # need to adjust maybe

        while (not self.dico.is_word(current_word_str)) and ite < max_ite:
            ite += 1
            possible_next = dico_tmp["next"].keys()
            if possible_next:
                next_letter = self.choose_letter(head,possible_next,authors_in_current_word)
                if next_letter is None:
                    current_word_str = ""
                    current_word = []
                    authors_in_current_word.clear()
                    dico_tmp = self.dico.dico
                else:
                    current_word_str += next_letter["letter"]
                    current_word.append(next_letter)
                    authors_in_current_word.add(next_letter["author"])
                    dico_tmp = dico_tmp["next"][next_letter["letter"]]

            else:
                current_word_str = ""
                current_word = []
                authors_in_current_word.clear()
                dico_tmp = self.dico.dico

        if ite == max_ite:
            return False,[]
        return True, current_word

    def choose_letter(self,head,possible,exclude_authors={}):
        choices = []
        self.cond.acquire()

        for letter in self.trletterpool[head]["letters"]:
            if (letter["letter"] in possible) and (not letter["author"] in exclude_authors):
                choices.append(letter)

        self.cond.release()
        if choices:
            return random.choice(choices)
        return None

    def inject_word(self, word, head):
        to_inject = {
            "word" : word,
            "head" : head,
            "politician" : self.pkstr,
            "signature" : crypto.sign_word(self.sk, word, head, self.pkstr)
        }
        server_coms.inject_word(self.socket, to_inject)
        blockchain.add_block(self.dico,self.trwordpool,to_inject)

    def handle_full_letterpool(self, pool):
        self.cond.acquire()
        self.trletterpool = letterpool.letterpool_to_trletterpool(pool)
        for letter in self.letterpool:
            letterpool.add_letter(self.trletterpool,letter)
        self.letterpool = []
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

    def handle_inject_letter(self, letter):
        self.cond.acquire()
        if self.trletterpool:
            letterpool.add_letter(self.trletterpool,letter)
        else:
            self.letterpool.append(letter)
        self.cond.release()
