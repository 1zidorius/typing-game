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
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.running = False
        self.word_spawn_timer = pygame.time.get_ticks()
        self.position = 0
        self.clock = pygame.time.Clock()

    def start(self):
        self.runLoop()
        self.stop()

    def runLoop(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                self.handleEvent(event)
            self.draw()
            pygame.display.update()

    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def draw(self):
        self.display_surface.fill(WHITE)
        timer = pygame.time.get_ticks()
        for i in range(200):
            self.render_text(self.display_surface, self.font, "tekstas", BLACK, (self.position + i, 0))

    def stop(self):
        pygame.quit()
        exit(0)

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


class Word:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vx = 2

    def update_object(self):
        self.x


g = Game()
g.start()

pygame.quit()
