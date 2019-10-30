import random
from acteur import Acteur
from dictionary import Dictionnary
import server_coms
import crypto

class Politicien(Acteur):
    def __init__(self, addr, port):
        Acteur.__init__(self, addr, port)
        self.dict = Dictionnary()
        self.dict.load_file("dict/dict_100000_5_15.txt")
        self.main_loop()

    def main_loop(self):
        self.start()
        server_coms.get_full_letterpool(self.socket)
        server_coms.listen(self.socket)

        

        self.cond.acquire()
        while not self.current_letterpool:
            try:
                self.cond.wait()
            except KeyboardInterrupt:
                exit(0)
        self.cond.release()

        word = self.choose_word()
        print(word)
        self.inject_word(word, self.head_block)

        self.stop()

    def choose_word(self): 
        # TODO VERY random and won't stop until it finds a match, even if it's impossible (but will take into account letters that are added while searching for a word)

        # TODO Stop once this period is over even if nothing was found, to focus on the next one
        
        current_word_str = ""
        current_word = []
        authors_in_current_word = []
        
        while not self.dict.is_word(current_word_str):
            # print(current_word_str)
            if(self.dict.exists_word_with_prefix(current_word_str)):
                next_letter = self.choose_letter(authors_in_current_word)
                if next_letter is None:
                    # Cannot create a word big enough to fit with this prefix
                    current_word_str = ""
                    current_word = []
                    authors_in_current_word.clear()
                    continue
                current_word_str += next_letter["letter"]
                current_word.append(next_letter)
                authors_in_current_word.append(next_letter["author"])
            else:
                current_word_str = ""
                current_word = []
                authors_in_current_word.clear()
        return current_word

    def choose_letter(self, exclude_authors=[]):
        letters = []
        self.cond.acquire()
        for l in self.current_letterpool:
            if not l[1]["author"] in exclude_authors:
                letters.append(l[1])
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
        # print(to_inject)
        server_coms.inject_word(self.socket, to_inject)

    # TODO ==== Define how to handle server responses in this class here ====

    def handle_letters_bag(self, letters):
        pass # Shouldn't happen

    def handle_next_turn(self, turn):
        self.cond.acquire()
        self.current_period = turn
        self.cond.notify_all()
        self.cond.release()

    def handle_full_letterpool(self, letterpool):
        self.cond.acquire()
        self.current_letterpool = letterpool["letters"]
        self.cond.notify_all()
        self.cond.release()

    def handle_full_wordpool(self, wordpool):
        self.cond.acquire()
        self.current_wordpool = wordpool["words"]
        self.cond.release()

    def handle_diff_letterpool(self, diff):
        # TODO Define
        print(diff)

    def handle_diff_wordpool(self, diff):
        # TODO Define
        print(diff)

    def handle_inject_letter(self, letter):
        print(letter)

        self.cond.acquire()
        if(letter["period"] == self.current_period):
            self.current_letterpool.append([letter["period"], letter])
            self.cond.notify_all()
        self.cond.release()

    def handle_inject_word(self, word):
        # TODO Define
        pass
    
    def handle_inject_raw_op(self, raw_op):
        # TODO Define
        pass

p = Politicien("localhost", 12346)