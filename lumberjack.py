import sys
import pygame


class Lumberjack:
    """Ogólna klasa do zarządzania sposobem działania gry"""

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((1200, 800))

        pygame.display.set_caption("Lumberjack")

    def run_game(self):
        """Rozpoczęcie pętli głównej gry"""

        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """Reakcje na zdarzenia generowane przez użytkownika"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_ESCAPE:
            sys.exit()

    def _update_screen(self):
        """Uaktualnianie obrazów na ekranie"""
        self.screen.fill(0, 0, 0)

        pygame.display.flip()
        self.clock.tick(60)


if __name__ == '__main__':
    # Utworzenie egzemplarza gry i jej uruchomienie
    lj = Lumberjack()
    lj.run_game()
