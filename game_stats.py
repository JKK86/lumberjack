class GameStats:
    def __init__(self, lj_game):
        self.settings = lj_game.settings
        self.game_active = True
        self.lives_left = self.settings.lives_limit
        self.time_left = self.settings.time_limit
        self.score = 0
        self.level = 1
