import argparse
import collections
import logging
import os
import sys

import pygame as pg
from pygame.locals import *


EVT_TICK = USEREVENT


def parse_args():
    a = argparse.ArgumentParser()
    a.add_argument("-v", "--verbose", help="Increase logging verbosity", default=False, action="store_true")
    return a.parse_args()


class ChordList(collections.deque):
    pass


class Chord(object):
    def __init__(self,
                 chord,
                 duration=60,
                 buffer=5):
        self._chord = chord

        self._pre = buffer
        self._duration = duration
        self._post = buffer

    def tick(self):
        if self._pre > 0:
            self._pre -= 1
            return self._pre + 1

        if self._duration > 0:
            self._duration -= 1
            return self._duration + 1

        if self._post > 0:
            self._post -= 1
            return self._post + 1

    def finished(self):
        return False if self._pre + self._duration + self._post > 0 else True

    def __repr__(self):
        return "{} to {}".format(*self._chord)


def process_tick(chord, screen, fonts, bg):
    num = chord.tick()

    (s_w, s_h) = screen.get_size()

    screen.blit(bg, (0, 0))

    color = (128, 255, 10)
    text_num = fonts['big'].render(str(num), True, color)
    text_chord = fonts['small'].render(str(chord), True, (150, 180, 230))

    (tn_w, tn_h) = text_num.get_size()
    (tc_w, tc_h) = text_chord.get_size()

    changed = screen.blit(text_num, (s_w/2 - tn_w/2, s_h/2 - tn_h/2 - 50))
    screen.blit(text_chord, (s_w/2 - tc_w/2, changed.bottom + 20))
    pg.display.flip()


def init_app():
    screen = pg.display.set_mode((640, 480), pg.RESIZABLE)
    pg.display.set_caption("Guitar Assistant")

    bg = pg.Surface(screen.get_size())
    bg = bg.convert()
    bg.fill((5, 5, 5))

    screen.blit(bg, (0, 0))
    pg.display.flip()

    return screen, bg


def init_chords():
    return [
        ('D', 'E'),
        ('A', 'E'),
        ('D', 'A'),
        ('Am', 'Dm'),
        ('A', 'Dm'),
        ('E', 'Dm'),
        ('C', 'G'),
        ('D', 'G'),
        ('G', 'E'),
        ('C', 'E'),
        ('G7', 'C'),
        ('C7', 'Fmaj7'),
        ('C7', 'G7'),
        ('Fmaj7', 'A'),
        ('F', 'C'),
        ('B7', 'E'),
        ('F', 'G'),
        ('F', 'Dm'),
        ('Fm7', 'B7'),
        ('D7', 'E7'),
        ('A7', 'D7'),
    ]


def main():
    pg.init()

    (screen, bg) = init_app()

    fonts = {
        'big': pg.font.SysFont("Arial", 192, True),
        'small': pg.font.SysFont("Arial", 48, True),
    }

    chord_list = ChordList(init_chords())
    chord = None

    pg.time.set_timer(EVT_TICK, 1000)

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                return

            if event.type == EVT_TICK:
                try:
                    if not chord or chord.finished():
                        chord = Chord(chord_list.popleft())

                    process_tick(chord, screen, fonts, bg)
                except IndexError:
                    return


if __name__ == "__main__":
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    main()
