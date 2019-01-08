"""
Classes to train genetic bots
"""
from time import sleep
from games.game import Session
from renderers import NullRenderer, TerminalRenderer


class BotTrainer(object):
    """
    Breeds bots until one can win the game
    """
    def __init__(
            self,
            game_factory,
            bot_factory,
            generation_size,
            max_mutations,
            min_mutations=1,
            max_generations=10000,
            max_turns=100,
            goal_score=None,
            game_renderer_factory=NullRenderer,
            progress_renderer_factory=TerminalRenderer
    ):
        # TODO: Reduce state
        self.game_factory = game_factory
        self.bot_factory = bot_factory
        self.generation_size = generation_size
        self.max_mutations = max_mutations
        self.min_mutations = min_mutations
        self.max_generations = max_generations
        self.max_turns = max_turns
        self.goal_score = float(goal_score) if goal_score is not None else None
        self.game_renderer_factory = game_renderer_factory
        self.progress_renderer_factory = progress_renderer_factory

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
        with self.progress_renderer_factory().render_context() as progress_ctx:
            with self.game_renderer_factory().render_context() as game_ctx:
                while True:
                    self._do_progress(generations, best_result, progress_ctx)
                    next_best_result = self.test_generation(
                        bots, best_result, game_ctx)
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

    def _do_progress(self, generation, best_result, render_context):
        msg = 'Testing generation {}'.format(generation)
        if self.goal_score is not None:
            msg += ' ({:.2%})'.format(best_result.score / self.goal_score)
        msg += '...'

        render_context.reset_frame()
        render_context.draw_text_array([msg])
        sleep(0.5)

    def _breed(self, bot):
        bots = []
        controls = self.game_factory().player_controls()
        for _ in xrange(self.generation_size):
            bots.append(bot.reproduce(
                controls, self.min_mutations, self.max_mutations
            ))
        return bots
