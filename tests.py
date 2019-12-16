import pytest

from word import Word


def test_word_initial_velocity():
    word = Word()
    assert word.velocity == 2


def test_word_x_position_after_1_update():
    word = Word()
    word.update()
    assert word.x == 2


def test_word_x_position_after_5_updates():
    word = Word()
    for i in range(5):
        word.update()
    assert word.x == 10
