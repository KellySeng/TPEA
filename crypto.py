import nacl.signing as nas
import nacl.encoding as nae
from nacl.exceptions import BadSignatureError

def pkstr_of_pk(pk):
    """Return the public key in string from the verify key object"""
    return pk.encode(encoder=nae.HexEncoder).decode()

def pk_of_pkstr(pkstr):
    """Return the verify key object from the public key in string """
    return nas.VerifyKey(pkstr.encode(),encoder=nae.HexEncoder)

def keyGen():
    """Generate a pair of signing key and verify key"""
    sk = nas.SigningKey.generate()
    pk = sk.verify_key
    return pk, sk

def sign(sk,data):
    """Sign the message with the signing key"""
    return sk.sign(data.encode()).signature

def verify(pkstr,data, signature):
    """Verify the date with a signature and a public key"""
    try:
        pk = pk_of_pkstr(pkstr)
        pk.verify(data.encode(), signature)
        return True
    except (BadSignatureError):
        return False
