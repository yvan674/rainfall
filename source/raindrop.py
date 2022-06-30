"""Raindrop.

Class which represents a single raindrop.
"""

class Raindrop:
    def __init__(self, x: int, y: int, drop_str: str, color: str = None):
        """Creates a raindrop.

        Args:
            x: The x coordinate of the raindrop.
            y: The y coordinate of the raindrop.
            drop_str: The shape of the raindrop.
            color: The color of the raindrop.
        """
        self.x = x
        self.y = y
        self.drop_str = drop_str
        self.color = color
