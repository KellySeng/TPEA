from Acteur import Acteur
import random
import string
import json
import hashlib
import binascii
import nacl.signing as nas
import nacl.encoding as nae
from nacl.exceptions import BadSignatureError

class Auteur(Acteur):

    def generateLetter(self):
        random.choice(string.ascii_letters).lower()

    def byte_to_binary(n):
        return ''.join(str((n & (1 << i)) and 1) for i in reversed(range(8)))
    
    def injectLetter(self,letter,period,hash_pred,author):

        if(len(letter) ==1 ):
                x = {
                    "letter" : letter,
                    "period" : period, #taille du message 8 bytes qui encodent la taille en binaire
                    "head" : hash_pred,
                    "author" :  author      #self.pk.encode(encoder=nae.HexEncoder)
                }

                letter_bin = ''.join(format(ord(i), 'b') for i in letter) 
                print(letter_bin)
                period_bin = "{0:b}".format(period)
                print(period_bin)
                binary = lambda x: "".join(reversed( [i+j for i,j in zip( *[ ["{0:04b}".format(int(c,16)) for c in reversed("0"+x)][n::2] for n in [1,0] ] ) ] ))
                head_bin = binary(hash_pred)
                print(head_bin)
               # author_bin = bin(int(self.pk.encode(encoder=nae.HexEncoder), base=16)).lstrip('0b')
                author_bin = bin(int(author,base=16)).lstrip('0b')
                print(author_bin)

                concat = letter_bin + period_bin + head_bin + author_bin
                m = hashlib.sha256()
                m.update(concat.encode())
                res_concat = m.hexdigest()
                print(res_concat)
                sig = self.sign(res_concat)
                print(sig)
                print(self.verify(self.pk,res_concat,  self.sign(res_concat)))

                x["signature"] = sig
                data = json.dumps(x)

                return data
a = Auteur()
a.injectLetter("a",0,"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca","b7b597e0d64accdb6d8271328c75ad301c29829619f4865d31cc0c550046a08f")