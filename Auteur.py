from Acteur import Acteur
import random
import string
import json
import hashlib
import binascii
import nacl.signing as nas
import nacl.encoding as nae
from nacl.exceptions import BadSignatureError
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
        self.injectLetter(self.generateLetter(), self.current_period, self.head_block, self.pkstr)
        self.stop()
        #Define main  routine here

    def generateLetter(self):
        if(len(self.letters_bag) > 0):
            return random.choice(self.letters_bag)
        else:
            return None

    def byte_to_binary(self, n):
        return ''.join(str((n & (1 << i)) and 1) for i in reversed(range(8)))
    
    def injectLetter(self, letter, period, hash_pred, author):

        if(len(letter) == 1):
            to_inject = {
                "letter" : letter,
                "period" : period, #taille du message 8 bytes qui encodent la taille en binaire
                "head" : hash_pred,
                "author" :  author      #self.pk.encode(encoder=nae.HexEncoder)
            }

            hasher = hashlib.sha256()

            letter_bin = ord(letter).to_bytes(1, byteorder="big")
            hasher.update(letter_bin)
            
            period_bin = (period).to_bytes(8, byteorder="big")
            hasher.update(period_bin)
            
            head_bin = int(hash_pred, 16).to_bytes(32, byteorder="big")
            hasher.update(head_bin)
            
            author_bin = int(author, 16).to_bytes(32, byteorder="big")
            hasher.update(author_bin)
            

            res_concat = hasher.digest()
            sig = crypto.sign(self.sk, res_concat)
            to_inject["signature"] = sig
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

        
a = Auteur("localhost", 12346)

