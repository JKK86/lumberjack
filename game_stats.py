class GameStats:
    def __init__(self, lj_game):
        self.settings = lj_game.settings
        self.game_active = False
        self.high_score = 0
        self.reset_stats()

    def reset_stats(self):
        """Inicjalizacja danych statystycznych zmieniających się w czasie gry"""
        self.lives_left = self.settings.lives_limit
        self.time_left = self.settings.time_limit
        self.score = 0
        self.level = 1
