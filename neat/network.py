"""
Classes for Neural Net learning via NEAT
NeuroEvolution of Augmenting Topologies
Video that inspired this entire machine-learning project:
    https://www.youtube.com/watch?v=qv6UVOQ0F44
Original NEAT paper (that I didn't read):
    http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf
"""
from copy import deepcopy
import random


class Neuron(object):
    """
    Base Network Node
    """
    def __init__(self):
        self.outputs = {}

    def eval(self, hot, traversal):
        return hot

    def simulate(self, hot, traversal):
        hot = self.eval(hot, traversal)
        traversal[self] = traversal.get(self, False) or hot
        for neuron, polarity in self.outputs.iteritems():
            # TODO: A proper negative connection should override
            # other connections
            neuron.simulate(polarity == hot, traversal)


class GameStateNeuron(Neuron):
    """
    Neuron is 'activated' by something in the game state
    """
    def __init__(self, state_extractor):
        super(GameStateNeuron, self).__init__()
        self.state_extractor = state_extractor

    def eval(self, hot, traversal):
        return self.state_extractor(traversal.game.state)


class Network(object):
    """
    Neural Network
    """
    def __init__(self, input_layer, output_layer, middle_layer=None):
        self.inputs = deepcopy(input_layer)
        self.outputs = deepcopy(output_layer)
        self.middle = deepcopy(middle_layer) if middle_layer else []

    def traverse(self):
        traversal = {}
        for node in self.inputs:
            node.simulate(True, traversal)
        return traversal

    def add_random_neuron(self, allow_middle=True, factory=Neuron):
        edge = self._create_canidate_edge(allow_middle)
        new_input, input_polarity, new_output, output_polarity = edge

        node = factory()
        node.outputs[new_output] = output_polarity
        new_input.outputs[node] = input_polarity
        self.middle.append(new_input)

    def add_random_connection(self):
        edge = self._create_canidate_edge()
        new_input, input_polarity, new_output, output_polarity = edge

        # TODO: Is it ok to connect an input directly to an output?
        new_input.outputs[new_output] = input_polarity

    def _create_canidate_edge(self, allow_middle=True):
        input_polarity = random.choice((True, False))
        output_polarity = random.choice((True, False))

        input_choices = self.inputs
        if allow_middle:
            input_choices += self.middle
        new_input = random.choice(input_choices)

        output_choices = self.outputs
        if allow_middle:
            output_choices += self.middle
        output_choices = [_ for _ in output_choices if _ != new_input]
        new_output = random.choice(output_choices)

        return new_input, input_polarity, new_output, output_polarity
