"""
Base Classes for simple games
"""


class Game(object):
    """
    Base Game object
    """

    def tick(self, move):
        """
        Manipulate the game state with a discreet action
        """
        raise NotImplementedError

    def in_progress(self):
        """
        Determine if the game is currently in progress
        """
        raise NotImplementedError

    def render(self, output):
        """
        Render the game state
        """
        raise NotImplementedError


class Session(object):
    """
    Let a player play a game
    """
    def __init__(self, game, player, renderer):
        self.game = game
        self.player = player
        self.renderer = renderer

    def play(self):
        """
        Loop over a game
        """
        self.render()
        while self.game.in_progress():
            self.game.tick(self.player.next_move(self.game))
            self.render()

    def render(self):
        """
        Render the game state
        """
        self.renderer.reset_frame()
        self.game.render(self.renderer)
