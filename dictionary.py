# On utilise un arbre lexicographique pour stocker les mots d'un fichier
# La structure est de la forme suivante
# arbre : {"is_word : <bool>, "next" : <map<str,arbre>>}
# Le champ "is_word" indique si le parcours de la racine jusqu'a ce noeud est un mot
# Ensuite le champ "next" est une map avec pour clefs les lettres suivantes possible
# et les valeurs des sous arbres lexicographique pour continuer a former des mots

class Dictionary:

    def __init__(self):
        self.dico = self.empty_dictionary()
        self.score = {
            "a" : 1,
            "b" : 3,
            "c" : 3,
            "d" : 2,
            "e" : 1,
            "f" : 4,
            "g" : 2,
            "h" : 4,
            "i" : 1,
            "j" : 8,
            "k" : 10,
            "l" : 1,
            "m" : 2,
            "n" : 1,
            "o" : 1,
            "p" : 3,
            "q" : 8,
            "r" : 1,
            "s" : 1,
            "t" : 1,
            "u" : 1,
            "v" : 4,
            "w" : 10,
            "x" : 10,
            "y" : 10,
            "z" : 10
        }

    def empty_dictionary(self):
        """
        Return an empty dictionary
        """
        return {"is_word" : False, "next":{}}

    def add_word(self,word):
        """
        Add a new word in the dictionary
        """
        tmp = self.dico
        letters = self.dico["next"]
        for x in word:
            if x in letters:
                tmp = letters[x]
                letters = tmp["next"]
            else:
                tmp = self.empty_dictionary()
                letters[x] = tmp
                letters = tmp["next"]
        tmp["is_word"] = True

    def is_word(self,word):
        """
        Check if a word is in the dictionary
        """
        tmp = self.dico
        letters = self.dico["next"]
        for x in word:
            if x in letters:
                tmp = letters[x]
                letters = tmp["next"]
            else:
                return False
        return tmp["is_word"]

    def load_file(self,namefile):
        """
        Create a dictionary from a file containing a word per line
        """
        self.dico = self.empty_dictionary()
        f = open(namefile,"r")
        for tmp in f:
            line = tmp[:-1]
            self.add_word(line)

    def score_word(self,word):
        """
        Give the score of a word
        """
        if not(self.is_word(word)):
            return 0
        score = 0
        for x in word:
            score += self.score[x]
        return score

    def score_letter(self,letter):
        """
        Give the score of a letter
        """
        return self.score[letter]
