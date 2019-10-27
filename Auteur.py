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
        # self.main_loop # TODO Uncomment once main loop is defined

    def main_loop(self):
        #Define main  routine here
        pass

    def generateLetter(self):
        random.choice(string.ascii_letters).lower()

    def byte_to_binary(self, n):
        return ''.join(str((n & (1 << i)) and 1) for i in reversed(range(8)))
    
    def injectLetter(self,letter,period,hash_pred,author):

        if(len(letter) == 1 ):
                x = {
                    "letter" : letter,
                    "period" : period, #taille du message 8 bytes qui encodent la taille en binaire
                    "head" : hash_pred,
                    "author" :  author      #self.pk.encode(encoder=nae.HexEncoder)
                }

                letter_bin = bin(ord(letter)).lstrip("0b").zfill(8)
                print(letter_bin)
                period_bin = "{0:b}".format(period).zfill(64) # TODO Not sure if that is big endian order
                print(period_bin)
                head_bin = bin(int(hash_pred, 16)).lstrip("0b").zfill(256)
                print(head_bin)
                author_bin = bin(int(author, 16)).lstrip('0b').zfill(256)
                print(author_bin)

                concat = letter_bin + period_bin + head_bin + author_bin
                m = hashlib.sha256()
                m.update(concat.encode())
                res_concat = m.hexdigest()
                print(res_concat)
                sig = crypto.sign(self.sk, res_concat.encode())
                print(sig)
                print(crypto.verify(self.pkstr, res_concat.encode(), crypto.sign(self.sk, res_concat.encode())))

                x["signature"] = sig
                print(x)
                server_coms.inject_letter(self.socket, x)

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
a.start()
a.injectLetter("a",0,"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", a.pkstr)
a.stop()
