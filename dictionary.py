class Dictionnary:

    def __init__(self):
        self.dico = self.empty_dictionary()

    def empty_dictionary(self):
        return {"is_word" : False, "next":{}}

    def add_word(self,word):
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
        self.dico = self.empty_dictionary()
        f = open(namefile,"r")
        for tmp in f:
            line = tmp[:-1]
            self.add_word(line)
