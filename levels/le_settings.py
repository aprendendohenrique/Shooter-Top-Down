class LESettings:

    def __init__(self):
        self._screen_size = 500  # 720 is 1280 by 720 (16:9)
        self.screen_resolution = self._screen_size * 1.78, self._screen_size
        self.background_color = (200, 200, 200)

        self.fps = 60

        self.TILE_SIZE = 32