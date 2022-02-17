import string


class GameStats:
    def __init__(self, lj_game):
        self.settings = lj_game.settings
        self.game_active = False
        self.highscores = []
        self.name = ""
        with open('highscores.txt', 'r') as file:
            for line in file:
                if len(line) < 2:
                    continue
                split_lines = line.split()
                self.highscores.append((split_lines[0], int(split_lines[1])))
        self.high_score = self.highscores[0][1]
        self.reset_stats()

    def check_highscores_list(self):
        if self.score > int(self.highscores[-1][1]):
            return True
        else:
            return False

    def save_score(self):
        self.highscores.append((self.name, self.score))
        self.highscores.sort(key=lambda x: -x[1])
        if len(self.highscores) > 10:
            self.highscores.pop()
        lines = []
        for name, score in self.highscores:
            lines.append(f'{name} {score}\n')
        with open('highscores.txt', 'w') as file:
            file.writelines(lines)

    def set_player_name(self, key):
        if key.name == "BACKSPACE" and self.name:
            self.name = self.name[:-1]
        elif len(self.name) < 10:
            if key.name in string.ascii_letters.lower() + string.digits:
                self.name += key.name
        elif key.name == "RETURN":
            self.save_score()

    def draw(self):
        for i, line in enumerate(self.highscores):
            name, score = line

    def reset_stats(self):
        """Inicjalizacja danych statystycznych zmieniających się w czasie gry"""
        self.lives_left = self.settings.lives_limit
        self.time_left = self.settings.time_limit
        self.score = 0
        self.level = 1
