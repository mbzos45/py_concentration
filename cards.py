from __future__ import annotations

import random
import pygame as pg
import enum

IMG_PATH = "assets/img/"
CARD_BACK_NAME = "cardBack.png"
CARD_GAP = (40, 50)


class Suit(enum.IntEnum):
    SPADES = 1
    CLUBS = 2
    DIAMONDS = 3
    HEARTS = 4


class Score(enum.IntEnum):
    A = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    J = 11
    Q = 12
    K = 13

    def get_str(self):
        if self.value == Score.A:
            result = "A"
        elif self.value == Score.J:
            result = "J"
        elif self.value == Score.Q:
            result = "Q"
        elif self.value == Score.K:
            result = "K"
        else:
            result = str(self.value)
        return result


class Card:
    def __init__(self, suit: Suit, score: Score, back_surface: pg.Surface | pg.SurfaceType,
                 front_surface: pg.Surface | pg.SurfaceType, x=0, y=0):
        self.SUIT = suit
        self.SCORE = score
        self.back_surface = pg.transform.scale(back_surface, tuple(map(lambda a: a / 2, back_surface.get_size())))
        self.front_surface = pg.transform.scale(front_surface, tuple(map(lambda a: a / 2, front_surface.get_size())))
        self.is_opened = False
        self.surface = self.back_surface
        self.is_cleared = False
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y

    def open_card(self):
        self.surface = self.front_surface
        self.is_opened = True

    def hide_card(self):
        self.surface = self.back_surface
        self.is_opened = False

    def clear_card(self):
        self.is_cleared = True


def get_front_img(suit: Suit, score: Score):
    path = IMG_PATH + "card" + suit.name.capitalize() + score.get_str() + ".png"
    return pg.image.load(path)


def init_cards() -> list[list[Card | None]]:
    back_img = pg.image.load(IMG_PATH + CARD_BACK_NAME)
    raw_list = [Card(suit, score, back_img, get_front_img(suit, score)) for suit in Suit for score in Score]
    random.shuffle(raw_list)
    suit_len = len(Suit)
    score_len = len(Score)
    result = [raw_list[i:i + score_len] for i in range(0, suit_len * score_len, score_len)]
    card_size = result[0][0].surface.get_size()
    y_pos = 10
    for single_list in result:
        x_pos = 10
        for card in single_list:
            card.rect.x = x_pos
            card.rect.y = y_pos
            x_pos += card_size[0] + CARD_GAP[0]
        y_pos += card_size[1] + CARD_GAP[1]
    return result
