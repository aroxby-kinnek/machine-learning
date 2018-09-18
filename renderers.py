"""
Game Renderers
"""
class PrintRenderer(object):
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
