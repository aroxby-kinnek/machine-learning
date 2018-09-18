"""
Players!
"""
from readchar import readchar

class HumanPlayer(object):
    """
    Human player input
    """
    def next_move(self, game):
        return readchar().upper()
