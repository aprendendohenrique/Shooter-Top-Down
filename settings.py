class Settings:
    """File that stores configurable information of the game"""

    def __init__(self):
        """General Settings"""
        self.fps = 60

        """Screen Settings"""
        self.screen_size = 500 # 720 is 1280 by 720 (16:9)
        self.screen_resolution = self.screen_size * 1.78, self.screen_size
        self.background_color = 0, 125, 0

        """Player Settings"""
        self.player_speed = 8
        self.bullet_speed = 10

        # Time in milliseconds(1000 milisec = 1 sec)
        self.bullet_despawn_time = 3000
        self.firerate = 500

