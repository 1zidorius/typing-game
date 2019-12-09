import pygame
import random

from settings import *


class Game:
    def __init__(self):
        self.playing = True
        self.playing_game = True
        self.success_count = 0
        pygame.init()
        self.lines_read = self.load_words_file("words.txt")  # load words from the file
        pygame.display.set_caption(TITLE)
        self.display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.speed = 2  # moving speed for texts
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.running = True

    def new(self):
        # start a new game
        self.run()

    def run(self):
        # Game loop
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        pass

    def events(self):
        words_on_screen = []
        typing_buffer = []
        current_text = ""
        word_spawn_timer = pygame.time.get_ticks()  # used for spawning words
        ended = False
        while self.playing_game:
            countdown_timer = GAME_LENGTH - (pygame.time.get_ticks() / 1000)
            if int(countdown_timer) <= 0:  # end game
                self.display_surface.fill(WHITE)
                self.render_text(self.display_surface, self.font, "Game over", BLACK, (300, 150))
                self.render_text(self.display_surface, self.font, f"Score: {self.success_count} words per minute",
                                 BLACK, (150, 250))
                ended = True
                self.playing_game = False
            if not ended:
                self.display_surface.fill(WHITE)
                if pygame.time.get_ticks() - word_spawn_timer > 1500:
                    word_spawn_timer = pygame.time.get_ticks()
                    self.release_wave(1, self.lines_read, words_on_screen)
                for word_info in words_on_screen:
                    # word_info["coordinate"] = (word_info["coordinate"][0] + self.speed, word_info["coordinate"][1])
                    word_info["coordinate"] = (word_info["coordinate"][0] + self.speed, 150)
                    self.render_text(self.display_surface, self.font, word_info["word"], BLACK, word_info["coordinate"])
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.playing_game = False
                        self.running = False
                    if event.type == pygame.KEYDOWN:
                        if pygame.key.name(event.key) == "return":
                            index_found = self.is_word_on_screen(words_on_screen, current_text)
                            if index_found != -1:
                                words_on_screen.pop(index_found)
                                self.success_count += 1
                            else:
                                print("wrong")
                            typing_buffer = []
                        else:
                            if pygame.key.name(
                                    event.key) == "backspace":  # if backspace then delete last element of typing buffer
                                if len(typing_buffer) != 0:
                                    typing_buffer.pop(len(typing_buffer) - 1)
                            else:
                                typing_buffer.append(pygame.key.name(event.key))
                        current_text = "".join(typing_buffer)
                self.render_text(self.display_surface, self.font, current_text, BLACK, (20, 450))
                self.render_text(self.display_surface, self.font, str(round(countdown_timer, 2)), BLACK, (600, 450))
                self.render_text(self.display_surface, self.font, f"Words {self.success_count}", BLACK, (10, 10))
            pygame.display.update()
            self.clock.tick(60)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def draw(self):
        pass

    def load_words_file(self, filename):
        word_file = open(filename, "r")
        lines_read = word_file.readlines()
        word_file.close()
        return lines_read

    def render_text(self, display_surface, font, text_content, color, position):
        text = font.render(text_content, True, color)
        display_surface.blit(text, position)

    def release_wave(self, count, lines_read, words_on_screen):  # count : how many words will be spawned
        for i in range(count):
            randomed = random.randrange(0, len(lines_read))
            randomed_word = lines_read[randomed].replace("\n", "")
            random_y = random.randrange(0, 500)
            words_on_screen.append({"word": randomed_word, "coordinate": (0, random_y)})

    def is_word_on_screen(self, words_on_screen, word):
        for i in range(len(words_on_screen)):
            if word == words_on_screen[i]["word"]:
                return i
        return -1

    def show_start_screen(self):
        pass


g = Game()
g.show_start_screen()
while g.running:
    g.new()

pygame.quit()
