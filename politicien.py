from acteur import Acteur
import server_coms

class Politicien(Acteur):
    def __init__(self, addr, port):
        Acteur.__init__(self, addr, port)
        # self.main_loop # TODO Uncomment once main loop is defined

    def main_loop(self):
        #Define main  routine here
        pass


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
