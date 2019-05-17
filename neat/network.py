"""
Classes for Neural Net learning via NEAT
NeuroEvolution of Augmenting Topologies
Video that inspired this entire machine-learning project:
    https://www.youtube.com/watch?v=qv6UVOQ0F44
Original NEAT paper (that I didn't read):
    http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf
"""
from __future__ import print_function
from copy import deepcopy
import random


class Neuron(object):
    """
    Base Network Node
    """
    class State(object):
        """
        Enum of neuron states
        """
        NEUTRAL = 0
        POSITIVE = 1
        NEGATIVE = 2

        def resolve(self, other):
            """
            Resolve compound state
            """
            return max(self, other)

    def __init__(self):
        self.outputs = {}

    def eval(self, hot, traversal):
        """
        Determine actual state (can be overridden)
        """
        return hot

    def simulate(self, hot, traversal):
        """
        Evaluate and propagate state
        """
        hot = self.eval(hot, traversal)
        traversal[self] = traversal.get(self, self.State.NEUTRAL) or hot
        for neuron, polarity in self.outputs.iteritems():
            neuron.simulate(polarity.resolve(hot), traversal)

    def print(self, **kwargs):
        """
        Print node info
        """
        output_hashes = [
            (polarity, hash(node))
            for polarity, node in self.outputs.iteritems()
        ]
        print(hash(self), '->', *output_hashes, **kwargs)


class Network(object):
    """
    Neural Network
    """
    def __init__(self, input_layer, output_layer, middle_layer=None):
        self.inputs = deepcopy(input_layer)
        self.outputs = deepcopy(output_layer)
        self.middle = deepcopy(middle_layer) if middle_layer else []

    def deep_copy(self):
        """
        Create a copy of the network
        """
        return self.__class__(self.inputs, self.outputs, self.middle)

    def traverse(self):
        """
        Evaluate network
        """
        traversal = {}
        for node in self.inputs:
            node.simulate(node.State.POSITIVE, traversal)
        return traversal

    def add_random_neuron(self, allow_middle=True, factory=Neuron):
        """
        Mutate network with a new neuron
        """
        edge = self._create_canidate_edge(allow_middle)
        new_input, input_polarity, new_output, output_polarity = edge

        node = factory()
        node.outputs[new_output] = output_polarity
        new_input.outputs[node] = input_polarity
        self.middle.append(new_input)

    def add_random_connection(self):
        """
        Mutate network with a new connection
        """
        edge = self._create_canidate_edge()
        new_input, input_polarity, new_output, _ = edge

        new_input.outputs[new_output] = input_polarity

    def _create_canidate_edge(self, allow_middle=True):
        possible_states = (Neuron.State.POSITIVE, Neuron.State.NEGATIVE)
        input_polarity = random.choice(possible_states)
        output_polarity = random.choice(possible_states)

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

    def print(self):
        """
        Print network info
        """
        for layer in [self.inputs, self.middle, self.outputs]:
            for node in layer:
                node.print(end=', ')
            print('')
