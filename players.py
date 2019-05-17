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
        mutations = random.randint(min_mutations, max_mutations)
        new_moves = self.moves[:]
        for _ in xrange(mutations):
            new_moves.append(random.choice(allowed_moves))
        return self.__class__(new_moves)


class NeatBot(BotPlayer):
    network_factory = GameNetwork()
    def __init__(self, network):
        self.games = {}
        self.network = network or self.network_factory()

    def next_move(self, game):
        moves = self.network.eval_game(game)
        # HACK
        preference = 'wasd'
        for move in preference:
            if move in moves:
                return move

        # HACK
        return 'Q'

    def reproduce(self, allowed_moves, min_mutations, max_mutations):
        mutations = random.randint(min_mutations, max_mutations)
        new_network = self.network.deep_copy()
        mutators = [    # FIXME: Add weights
            new_network.add_random_neuron,
            new_network.add_random_connection
        ]
        for _ in xrange(mutations):
            mutator = random.choice(mutators)
            mutator()
        return self.__class__(new_network)
