from neat.network import Network


class GameNeuron(Neuron):
    """
    Neuron is 'activated' by something in the game state
    """
    def __init__(self, state_extractor):
        super(GameStateNeuron, self).__init__()
        self.state_extractor = state_extractor

    def eval(self, hot, traversal):
        if self.state_extractor(traversal.game):
            return self.State.POSITIVE
        else:
            return self.State.NEUTRAL



class GameNetwork(Network):
    """
    Add methods to evaluate game state on network
    """
    def eval_game(game):
        """
        Ask the network to evaluate this game
        """
        pass
