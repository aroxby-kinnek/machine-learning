#!/usr/bin/env python
"""
Test harness
"""

from games.maze import Maze, Layout
from players import PlannedBot
from trainer import BotTrainer


def main():
    """
    Test harness
    """
    game_factory = lambda: Maze(Layout.from_string(Layout.EASY_STR))
    bot_factory = PlannedBot
    trainer = BotTrainer(game_factory, bot_factory, 4, 100, 2)
    result = trainer.breed_best_bot()
    print 'Bot score: ', result.score
    print 'Bot plan: ', result.player.moves


if __name__ == '__main__':
    main()
