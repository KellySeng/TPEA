from auteur import Auteur
import sys

addr = sys.argv[1]
port = 0
try:
    port = int(sys.argv[2])
except Exception:
    print("<port> must be an integer")
    exit(0)

namefile = sys.argv[3]

Auteur(addr,port,namefile)
