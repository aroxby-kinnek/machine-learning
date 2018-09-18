#!/usr/bin/env python
"""
Test harness
"""

import sys
from games.game import Session
from games.maze import Maze, Layout
from players import HumanPlayer
from renderers import PrintRenderer


def main():
    """
    Test harness
    """
    game = Maze(Layout.from_string(Layout.EASY_STR))
    player = HumanPlayer()
    renderer = PrintRenderer(sys.stdout)
    session = Session(game, player, renderer)
    session.play()


if __name__ == '__main__':
    main()
