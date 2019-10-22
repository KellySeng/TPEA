from Acteur import Acteur
import random
import string
import json
import nacl.signing as nas
import nacl.encoding as nae
from nacl.exceptions import BadSignatureError

class Auteur(Acteur):

    def __init__(self):
       Acteur.__init__(self)

    def generateLetter(self):
        random.choice(string.ascii_letters).lower()
    
    def injectLetter(self,letter,period,hash_pred):
        x = {
            "letter" : letter,
            "period" : period, #taille du message 8 bytes qui encodent la taille en binaire
            "head" : hash_pred,
            "author" : VerifyKey.objects.create(self.pk)[1]
        }

        #
        data = json.dumps(x)
        return x


a = Auteur()
a.injectLetter("a","10010100","0xbf541dsq")