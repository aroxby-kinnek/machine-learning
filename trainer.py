"""
Classes to train genetic bots
"""
from games.game import Session
from renderers import NullRenderer


class BotTrainer(object):
    """
    Breeds bots until one can win the game
    """
    def __init__(
            self,
            game_factory,
            bot_factory,
            generation_size,
            max_generations,
            max_mutations,
            min_mutations=1,
            max_turns=100,
            renderer_factory=NullRenderer,
    ):
        # TODO: Reduce state
        self.game_factory = game_factory
        self.bot_factory = bot_factory
        self.generation_size = generation_size
        self.max_generations = max_generations
        self.max_mutations = max_mutations
        self.min_mutations = min_mutations
        self.renderer_factory = renderer_factory
        self.max_turns = max_turns

    def test_bot(self, bot):
        """
        Test the bot against the game
        """
        game = self.game_factory()
        renderer = self.renderer_factory()
        session = Session(game, bot, renderer)
        return session.play(self.max_turns)

    def test_generation(self, bots, min_result):
        """
        Test a set of bots for the best
        """
        for bot in bots:
            result = self.test_bot(bot)
            if result > min_result:
                min_result = result
        return min_result

    def breed_best_bot(self):
        """
        Breeds the best random bot inside parameters
        """
        best_result = Session.Result.zero()
        best_bot = self.bot_factory()
        best_result.player = best_bot
        bots = [best_bot]
        generations = 0
        while not best_result.finished:
            next_best_result = self.test_generation(bots, best_result)
            next_best_bot = next_best_result.player
            if next_best_bot is not None and next_best_result > best_result:
                best_result = next_best_result
                best_bot = next_best_bot
            generations += 1
            if generations > self.max_generations:
                break
            else:
                bots = self._breed(best_bot)
        return best_result

    def _breed(self, bot):
        bots = []
        for _ in xrange(self.generation_size):
            bots.append(bot.reproduce(self.min_mutations, self.max_mutations))
        return bots
