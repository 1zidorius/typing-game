from __future__ import annotations
from typing import Optional
import pygame

from settings import *
from word import Word, Subword


class GameMeta(type):
    _instance: Optional[Game] = None

    def __call__(self) -> Game:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Game(metaclass=GameMeta):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.running = True
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.success_count = 0

    def new(self):
        self.word_spawn_timer = pygame.time.get_ticks()
        self.subword_spawn_timer = pygame.time.get_ticks()
        self.words_on_screen = []
        self.typing_buffer = []
        self.typed_text = ""
        self.success_count = 0
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        self.show_game_over_screen()

    def update(self):
        self.countdown_timer = GAME_LENGTH - (pygame.time.get_ticks() / 1000)
        if int(self.countdown_timer) <= 0:
            self.playing = False

        if pygame.time.get_ticks() - self.word_spawn_timer > 1000:
            self.words_on_screen.append(Word())
            self.word_spawn_timer = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.subword_spawn_timer > 5000:
            self.words_on_screen.append(Subword())
            self.subword_spawn_timer = pygame.time.get_ticks()

        self.success_count_text = f'Score: {str(self.success_count)}'
        self.countdown_timer_text = str(round(self.countdown_timer, 2))

        if self.is_word_reach_screen_edge():
            self.playing = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == 'return':
                    # TODO: pop object from array if its outside screen
                    if self.is_word_on_screen(self.typed_text):
                        self.success_count += 1
                    else:
                        print("wrong")
                    self.typing_buffer = []

                else:
                    if pygame.key.name(event.key) == 'backspace':
                        if len(self.typing_buffer) != 0:
                            self.typing_buffer.pop(len(self.typing_buffer) - 1)
                    else:
                        self.typing_buffer.append(pygame.key.name(event.key))
                self.typed_text = "".join(self.typing_buffer)

    def draw(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.background, (0, 0))
        self.display_words()
        self.draw_text(self.typed_text, FONT_SIZE, WHITE, WIDTH / 2, HEIGHT - 50)
        self.draw_text(self.success_count_text, FONT_SIZE, WHITE, 70, 10)
        self.draw_text(self.countdown_timer_text, FONT_SIZE, WHITE, WIDTH - 50, 10)
        pygame.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.SysFont(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def display_words(self):
        for word in self.words_on_screen:
            self.draw_text(str(word), 32, WHITE, word.position.x, word.position.y)
            word.update()

    def is_word_on_screen(self, word):
        for i, item in enumerate(self.words_on_screen):
            if str(item) == word:
                self.words_on_screen.pop(i)
                return True
        return False

    def is_word_reach_screen_edge(self):
        for i, word in enumerate(self.words_on_screen):
            if word.position.x >= WIDTH:
                return True
        return False

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def show_game_over_screen(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.background, (0, 0))
        self.draw_text("GAME OVER", 32, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(f"Score: {self.success_count}", 32, WHITE, WIDTH / 2, HEIGHT / 2 - 50)
        pygame.display.flip()
        self.wait_for_key()


g = Game()
while g.running:
    g.new()
    g.show_game_over_screen()

pygame.quit()
