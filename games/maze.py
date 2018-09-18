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

    EASY_STR = (
        'xxx\n'
        'xex\n'
        'x x\n'
        'x x\n'
        'xsx\n'
        'xxx\n'
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

    def is_blocked(self, x, y):
        """
        Is the tile at x, y unreachable
        """
        ret = True
        if y < len(self.tiles):
            if x < len(self.tiles[y]):
                ret = self.tiles[y][x] == self.WALL
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
        self.controls = {
            'W': self.north,
            'A': self.west,
            'S': self.south,
            'D': self.east,
            'Q': self.quit,
        }

    def in_progress(self):
        return self.playing

    def all_controls(self):
        return self.controls.keys()

    def render(self, renderer):
        self.layout.render(renderer)

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
        if not self.layout.is_blocked(*new_pos):
            old_pos = self.pos
            self.layout.erase(*old_pos)
            self.layout.put_token(self.PLAYER_TOKEN, *new_pos)
            self.pos = new_pos
            if self.pos == self.layout.goal:
                self.layout.put_token(self.WIN_TOKEN, *new_pos)
                self.quit()
