from Acteur import Acteur
import random
import string

class Auteur(Acteur):
    def generateLetter(self):
        random.choice(string.ascii_letters).lower()

