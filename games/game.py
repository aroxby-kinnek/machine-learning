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
    class Result(object):
        """
        Holds session results
        """
        def __init__(self, game, player, score, turns, finished):
            self.game = game
            self.player = player
            self.score = score
            self.turns = turns
            self.finished = finished

        @classmethod
        def zero(cls):
            """
            Returns the least possible result
            """
            return cls(None, None, None, None, None)

        def __gt__(self, other):
            if self.finished > other.finished:
                return True
            elif self.finished == other.finished:
                if self.score > other.score:
                    return True
                elif self.score == other.score:
                    if self.turns > other.turns:
                        return True
            return False

    def __init__(self, game, player, renderer):
        self.game = game
        self.player = player
        self.renderer = renderer

    def play(self, max_turns=None):
        """
        Loop over a game
        """
        self.render()
        turn = 1
        finished = False
        while max_turns is None or turn <= max_turns:
            self.game.tick(self.player.next_move(self.game))
            self.render()
            finished = not self.game.in_progress()
            if finished:
                break
            turn += 1
        return self.Result(
            self.game, self.player, self.game.score, turn, finished)

    def render(self):
        """
        Render the game state
        """
        self.renderer.reset_frame()
        self.game.render(self.renderer)
        # Line break
        self.renderer.draw_text_array([''])
