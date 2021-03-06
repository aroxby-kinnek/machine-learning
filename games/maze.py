"""
Simple Maze Game
"""
from games.game import Game


class Layout(object):
    """
    Maze layout
    """
    GOAL = 'e'
    START = 's'
    WALL = 'x'
    EMPTY = ' '
    SOLUTION = '+'

    EASY_STR = (
        'xxx\n'
        'xex\n'
        'x+x\n'
        'x+x\n'
        'xsx\n'
        'xxx'
    )
    MEDIUM_STR = (
        'xxxxxxxxxxxx\n'
        'xxx    xxxxx\n'
        'xxx xxxxxxxx\n'
        'x+++++++++ex\n'
        'x+xxxx xxxxx\n'
        'x+xxxx    xx\n'
        'x+xxxxxxxxxx\n'
        'xsxxxxxxxxxx\n'
        'xxxxxxxxxxxx'
    )

    def __init__(self, tiles):
        self.tiles = tiles[:]
        self.start = self.find_start()
        self.goal = self.find_goal()

    @staticmethod
    def from_string(chars):
        """
        Create layout from ASCII
        """
        tiles = [[]]
        for char in chars:
            if char == '\n':
                tiles.append([])
            else:
                tiles[-1].append(char)
        return Layout(tiles)

    def render(self, renderer):
        """
        Draw the layout
        """
        renderer.draw_text_array(self.tiles)

    def _find_target(self, target):
        """
        Find a specific tile
        """
        y = 0
        for row in self.tiles:
            x = 0
            for tile in row:
                if tile == target:
                    return x, y
                x += 1
            y += 1
        return None

    def find_start(self):
        """
        Find start tile
        """
        return self._find_target(self.START)

    def find_goal(self):
        """
        Find goal tile
        """
        return self._find_target(self.GOAL)

    def get_token(self, x, y):
        """
        Retrieve the tile at x, y
        """
        ret = self.WALL
        if y < len(self.tiles):
            if x < len(self.tiles[y]):
                ret = self.tiles[y][x]
        return ret

    def erase(self, x, y):
        """
        Clear tile at x,y
        """
        self.put_token(self.EMPTY, x, y)

    def put_token(self, token, x, y):
        """
        Place a token in the layout
        """
        self.tiles[y][x] = token


class Maze(Game):
    """
    Maze game class
    """
    PLAYER_TOKEN = '*'
    WIN_TOKEN = '!'

    def __init__(self, layout):
        self.layout = layout
        self.score = 0
        self.playing = True
        self.pos = layout.start
        self.layout.put_token(self.PLAYER_TOKEN, *self.pos)
        self.game_controls = {
            'W': self.north,
            'A': self.west,
            'S': self.south,
            'D': self.east,
        }
        self.meta_controls = {
            'Q': self.quit,
        }
        self.controls = self.game_controls.copy()
        self.controls.update(self.meta_controls)
        self.win = False

    def in_progress(self):
        return self.playing

    def player_controls(self):
        return self.game_controls.keys()

    def render_state(self, renderer):
        self.layout.render(renderer)

    def render_game(self, renderer):
        self.render_state(renderer)
        renderer.draw_text_array(['Score: {}'.format(self.score)])

    def won(self):
        return self.win

    def bad_move(self):
        """
        Bad move handler
        """
        pass

    def tick(self, move):
        action = self.controls.get(move, self.bad_move)
        action()

    def north(self):
        self._move(0, -1)

    def south(self):
        self._move(0, 1)

    def east(self):
        self._move(1, 0)

    def west(self):
        self._move(-1, 0)

    def quit(self):
        self.playing = False

    def _move(self, dx, dy):
        new_pos = self.pos[0] + dx, self.pos[1] + dy
        dst_token = self.layout.get_token(*new_pos)
        if dst_token != self.layout.WALL:
            old_pos = self.pos
            self.layout.erase(*old_pos)
            self.layout.put_token(self.PLAYER_TOKEN, *new_pos)
            self.pos = new_pos
            if dst_token == self.layout.SOLUTION:
                self.score += 1
            elif dst_token == self.layout.GOAL:
                self.score += 1
                self.layout.put_token(self.WIN_TOKEN, *new_pos)
                self.win = True
                self.quit()
