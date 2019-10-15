from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15 as sg
from Cryptodome.Hash import SHA256
import base64

class Acteur:
    def KeyGen(self, length=1024):
        sk = RSA.generate(length)
        pk = sk.publickey()
        return pk, sk

    def sign(self, sk, data):
        h = SHA256.new(data.encode())
        return sg.new(sk).sign(h)    

    def verify(self, pk, data, signature):
        h = SHA256.new(data.encode())
        try:
            sg.new(pk).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False
        
# actor1 = Acteur()
# print(actor1.KeyGen())

msg = "Coucou"
a1 = Acteur()
pk,sk = a1.KeyGen()
s = a1.sign(sk, msg)
print(a1.verify(pk, msg, s))