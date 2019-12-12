import random


class Word:
    def __init__(self):
        self.x = 0
        self.y = 0
        self._words_pool = ['vienas', 'du', 'trys', 'keturi', 'penki', 'sesi', 'septyni', 'astuoni', 'devyni', 'desimt']
        self.velocity = 2
        self._word = self.get_random_word()

    def update(self):
        self.x += self.velocity

    def get_random_word(self):
        return self._words_pool[random.randrange(0, len(self._words_pool))]

    def __repr__(self):
        return self._word
