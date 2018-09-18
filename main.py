#!/usr/bin/env python
"""
Test harness
"""

from games.game import Session
from games.maze import Maze, Layout
from players import HumanPlayer
from renderers import TerminalRenderer


def main():
    """
    Test harness
    """
    game = Maze(Layout.from_string(Layout.EASY_STR))
    player = HumanPlayer()
    with TerminalRenderer().render_context() as renderer:
        session = Session(game, player, renderer)
        session.play()


if __name__ == '__main__':
    main()
