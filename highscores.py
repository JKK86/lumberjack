import string

import pygame

from landscape import LandscapeBaseClass


class Highscores:
    def __init__(self, lj_game):
        self.lj_game = lj_game
        self.screen = lj_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = lj_game.settings
        self.stats = lj_game.stats

        self.tag = LandscapeBaseClass(self.lj_game, 'wood_tag.png')

        self.board = LandscapeBaseClass(self.lj_game, 'wood_board2.png')
        self.text_color = self.settings.text_color
        self.font = pygame.font.Font('fonts/bungee-regular.ttf',
                                     int(20 * (self.screen.get_width() / self.settings.screen_width)))

        self.highscores = []
        self.name = ""

        self.load_highscores()

        self.high_score = self.highscores[0][1]

    def load_highscores(self):
        with open('highscores.txt', 'r') as file:
            for line in file:
                if len(line) < 2:
                    continue
                split_lines = line.split()
                self.highscores.append((split_lines[0], int(split_lines[1])))

    def check_highscores_list(self):
        if self.stats.score > int(self.highscores[-1][1]):
            return True
        else:
            return False

    def save_score(self):
        self.highscores.append((self.name, self.stats.score))
        self.highscores.sort(key=lambda x: -x[1])
        if len(self.highscores) > 10:
            self.highscores.pop()
        lines = []
        for name, score in self.highscores:
            lines.append(f'{name} {score}\n')
        with open('highscores.txt', 'w') as file:
            file.writelines(lines)

    def append_player_name(self, key):
        if key == "backspace" and self.name:
            self.name = self.name[:-1]
        if len(self.name) < 10:
            if key in string.ascii_letters.lower() + string.digits:
                self.name += key
        if key == "return" and self.name:
            self.save_score()
            self.lj_game.text_editor_mode = False

    def show_player_name(self):
        self.player_name = self.font.render("Your name: " + self.name, True, self.text_color)
        self.player_name_rect = self.player_name.get_rect()
        self.player_name_rect.center = self.tag.rect.center

        self.screen.blit(self.tag.image, self.tag.rect)
        self.screen.blit(self.player_name, self.player_name_rect)

    def draw(self):
        self.screen.blit(self.board.image, self.board.rect)
        headline = self.font.render("HIGHSCORES", True, self.settings.text_color)
        headline_rect = headline.get_rect()
        headline_rect.centerx = self.board.rect.centerx
        headline_rect.top = self.board.rect.top + 3
        for i, line in enumerate(self.highscores):
            name, score = line
            result_name = self.font.render(f"{i+1}. {name}", True, self.settings.text_color)
            result_score = self.font.render(f"{score}", True, self.settings.text_color)
            result_name_rect = result_name.get_rect()
            result_score_rect = result_score.get_rect()

            result_name_rect.left = self.board.rect.left + 10
            result_score_rect.right = self.board.rect.right - 10

            result_name_rect.top = self.board.rect.top + 26 * (i + 2)
            result_score_rect.top = self.board.rect.top + 26 * (i + 2)

            self.screen.blit(headline, headline_rect)
            self.screen.blit(result_name, result_name_rect)
            self.screen.blit(result_score, result_score_rect)
