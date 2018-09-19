"""
Players!
"""
from readchar import readchar


class Player(object):
    """
    Base player object
    """
    def next_move(self, game):
        """
        Retrieve the next move for this player in this game
        """
        raise NotImplementedError


class HumanPlayer(Player):
    """
    Human player input
    """
    def next_move(self, game):
        return readchar().upper()
