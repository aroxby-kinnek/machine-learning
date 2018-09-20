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
            game_renderer_factory=NullRenderer,
    ):
        # TODO: Reduce state
        self.game_factory = game_factory
        self.bot_factory = bot_factory
        self.generation_size = generation_size
        self.max_generations = max_generations
        self.max_mutations = max_mutations
        self.min_mutations = min_mutations
        self.game_renderer_factory = game_renderer_factory
        self.max_turns = max_turns

    def test_bot(self, bot, render_context):
        """
        Test the bot against the game
        """
        game = self.game_factory()
        session = Session(game, bot, render_context)
        return session.play(self.max_turns)

    def test_generation(self, bots, min_result, render_context):
        """
        Test a set of bots for the best
        """
        for bot in bots:
            result = self.test_bot(bot, render_context)
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
        with self.game_renderer_factory().render_context() as context:
            while True:
                next_best_result = self.test_generation(
                    bots, best_result, context)
                next_best_bot = next_best_result.player
                if (next_best_bot is not None and
                        next_best_result > best_result):
                    best_result = next_best_result
                    best_bot = next_best_bot
                if best_result.finished:
                    break
                generations += 1
                if generations > self.max_generations:
                    break
                else:
                    bots = self._breed(best_bot)
        return generations, best_result

    def _breed(self, bot):
        bots = []
        controls = self.game_factory().all_controls()
        for _ in xrange(self.generation_size):
            bots.append(bot.reproduce(
                controls, self.min_mutations, self.max_mutations
            ))
        return bots
