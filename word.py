import random


class Word:
    def __init__(self):
        self.x = 0
        self.y = 200
        self.words_pool = ['vienas', 'du', 'trys', 'keturi', 'penki', 'sesi', 'septyni', 'astuoni', 'devyni', 'desimt']
        self.velocity = 2
        self.word = self.get_random_word()

    def update(self):
        self.x += self.velocity

    def get_random_word(self):
        return self.words_pool[random.randrange(0, len(self.words_pool))]

    def __repr__(self):
        return self.word


class Subword(Word):
    def __init__(self):
        super().__init__()
        self.y = 250

    def update(self):
        self.x += self.velocity * 2
