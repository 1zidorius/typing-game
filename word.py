import random

from position import Position


class Word:
    def __init__(self):
        self.position = Position(0, 200)
        self.words_pool = ['vienas', 'du', 'trys', 'keturi', 'penki', 'sesi', 'septyni', 'astuoni', 'devyni', 'desimt']
        self.velocity = 2
        self.__word = self.get_random_word()

    def update(self):
        self.position.x += self.velocity

    def get_random_word(self):
        return self.words_pool[random.randrange(0, len(self.words_pool))]

    def __repr__(self):
        return self.__word


class Subword(Word):
    def __init__(self):
        super().__init__()
        self.position.y = 250

    def update(self):
        self.position.x += self.velocity * 2
