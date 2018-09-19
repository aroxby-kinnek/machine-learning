"""
Game Renderers
"""
import sys
from contextlib import contextmanager


class BaseRenderer(object):
    """
    Renderer Base
    """
    def render_context(self):
        """
        Activate the renderer
        """
        raise NotImplementedError


class RenderContext(object):
    """
    Render device handle
    """
    def draw_text_array(self, arr):
        """
        Draws an array of characters
        """
        raise NotImplementedError


class PrintRenderer(BaseRenderer, RenderContext):
    """
    Just dump everything to the screen/file
    """
    def __init__(self, output):
        self.output = output

    def draw_text_array(self, arr):
        """
        Draws an array of characters
        """
        for row in arr:
            self.output.write(''.join(row) + '\n')
        self.output.flush()

    def reset_frame(self):
        """
        Dummy method for compatibility
        """
        pass

    @contextmanager
    def render_context(self):
        """
        Dummy method for compatibility
        """
        yield self


class TerminalRenderer(BaseRenderer):
    """
    Grab the terminal and render to the same space over and over again
    """
    class LockedFile(object):
        """
        Drop-in replacement for file that blocks writing
        """
        def write(self, data):
            """
            Actually blocks write and print
            """
            raise RuntimeError('Print occurred during render')

    class Renderer(RenderContext):
        """
        Device Renderer
        """
        def __init__(self, output):
            self.output = output
            self.height = 0

        def reset_frame(self):
            """
            Reset the frame and prepare to draw again
            """
            # Terminal controls:
            # \x1b[A - Move up
            # \x1b[2K - Clear line
            self.output.write('\x1b[2K\x1b[A' * self.height)
            self.output.write('\x1b[2K\r')
            self.output.flush()
            self.height = 0

        def draw_text_array(self, arr):
            """
            Draws an array of characters
            """
            for row in arr:
                self.output.write(''.join(row) + '\n')
                self.height += 1
            self.output.flush()

    @contextmanager
    def render_context(self):
        if isinstance(sys.stdout, self.LockedFile):
            raise RuntimeError('Overlapping render contexts')

        stdout = sys.stdout
        stderr = sys.stderr
        sys.stdout = self.LockedFile()
        sys.stderr = self.LockedFile()

        try:
            yield self.Renderer(stdout)
        finally:
            sys.stderr = stderr
            sys.stdout = stdout
