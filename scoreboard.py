import pygame.font


class Scoreboard:
    """Klasa przeznaczona do przedstawianie informacji o punktacji i czasie gry"""

    def __init__(self, lj_game):
        """Inicjalizacja atrybutów dotyczących punktacji i timera"""
        self.lj_game = lj_game
        self.screen = lj_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = lj_game.settings
        self.stats = lj_game.stats

        # Ustawienia czcionki dla informacji dotyczącej punktacji
        self.text_color = self.settings.text_color
        self.font = pygame.font.Font('fonts/bungee-regular.ttf',
                                     int(20 * (self.screen.get_width() / self.settings.screen_width)))

        # Przygotowanie początkowch obrazów z punktacją
        self.prep_score()
        # self.prep_high_score()
        # self.prep_level()
        # self.prep_lives()

    def prep_score(self):
        """Przekształcenie punktacji na wygenerowany obraz"""
        score_str = f"{self.stats.score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Wyświetlanie punktacji, liczby statków i aktualnego poziomu na ekranie"""
        self.screen.blit(self.score_image, self.score_rect)
