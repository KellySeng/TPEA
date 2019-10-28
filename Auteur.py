from Acteur import Acteur
import random
import string
import json
import hashlib
import binascii
import crypto
import nacl.signing as nas
import nacl.encoding as nae
from nacl.exceptions import BadSignatureError
import server_coms
import time
import struct 

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
    
    # TODO ==== remplace hash_period by an instace of a blockchain
    def injectLetter(self,letter,period,hash_pred,author):

        # when the blockchain is empty
        empty = ""
        h = hashlib.sha256()
        h.update(empty.encode())
        hash_pred = h.hexdigest()


        if(len(letter) == 1 ):
            x = {
                "letter" : letter,
                "period" : period, #taille du message 8 bytes qui encodent la taille en binaire
                "head" : hash_pred,                  
                "author" :  author      #self.pk.encode(encoder=nae.HexEncoder)
            }
            
            #convert the letter to binary
            letter_binary = bin(ord(letter)).lstrip("0b").zfill(8)
        
            #convert the period to binary
            period_byte  = period.to_bytes((period.bit_length() + 7) // 8, 'big') or b'\0'    
            period_binary = bin(int(period_byte.hex(), base=16)).lstrip('0b').zfill(64)
    
            #convert the head to binary
            head_binary = bin(int(hash_pred, 16)).lstrip("0b").zfill(256)
         
            #convert the author public key to binary
            author_binary = bin(int(author, 16)).lstrip('0b').zfill(256)
         
            #concat everything and produce a hash
            concat = letter_binary + period_binary + head_binary + author_binary
            m = hashlib.sha256()
            m.update(concat.encode())
            res_concat = m.hexdigest()

            #add the signature to data
            sig = crypto.sign(self.sk, res_concat.encode())
            x["signature"] = sig
            
            #send the message to the server
            server_coms.inject_letter(self.socket, x)


    def get_letter_pool(self):
        server_coms.get_full_letterpool(self.socket)


    # TODO ==== Define how to handle server responses in this class here ====

    def handle_letters_bag(self, letters):
        print(letters)

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
a.injectLetter("a",0,"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca","b7b597e0d64accdb6d8271328c75ad301c29829619f4865d31cc0c550046a08f")
time.sleep(2)
a.get_letter_pool()
a.stop()