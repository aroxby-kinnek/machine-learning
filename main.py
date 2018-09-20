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
    def game_factory():
        """
        Creates the game we need
        """
        return Maze(Layout.from_string(Layout.EASY_STR))

    bot_factory = PlannedBot
    trainer = BotTrainer(game_factory, bot_factory, 4, 100, 2)
    generations, result = trainer.breed_best_bot()

    msg = 'After {} generations, the bot {} the game'.format(
        generations, 'won' if result.finished else 'lost')
    print msg
    print 'Bot score: ', result.score
    print 'Bot plan: ', result.player.moves


if __name__ == '__main__':
    main()
