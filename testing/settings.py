from encodings.punycode import selective_len


class Settings:
    """Class that stores all general settings for the game."""

    def __init__(self):
        # Game settings
        self.fps = 60

        # Screen settings
        self.screen_height = 500
        self.screen_resolution = self.screen_height * 1.78, self.screen_height
        self.background_color = 180, 180, 180
