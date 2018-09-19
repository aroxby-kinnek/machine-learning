"""
Players!
"""
import random
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


class BotPlayer(Player):
    """
    Base bot player
    """
    def reproduce(self, allowed_moves, min_mutations, max_mutations):
        """
        Create a new bot based on this bot
        """
        raise NotImplementedError


class PlannedBot(BotPlayer):
    """
    Bot is "born" with a fixed set of moves
    """
    def __init__(self, moves=None):
        self.moves = moves or []
        self.games = {}

    def next_move(self, game):
        idx = self.games.get(game, 0)
        self.games[game] = idx + 1
        if idx < len(self.moves):
            return self.moves[idx]
        # HACK
        return 'Q'

    def reproduce(self, allowed_moves, min_mutations, max_mutations):
        """
        Create a new bot based on this bot
        """
        # HACK
        allowed_moves = [move for move in allowed_moves if move != 'Q']
        mutations = random.randint(min_mutations, max_mutations)
        new_moves = self.moves[:]
        for _ in xrange(mutations):
            new_moves.append(random.choice(allowed_moves))
        return self.__class__(new_moves)
