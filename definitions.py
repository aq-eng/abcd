
from __future__ import print_function

import random
import unittest
import time

CATEGORY_TO_NUMBER = {
    "StreetFlush": 9,
    "Quads": 8,
    "FullHouse": 7,
    "Flush": 6,
    "Street": 5,
    "Trips": 4,
    "TwoPair": 3,
    "OnePair": 2,
    "HighCard": 1,
    "NoMatch": 0,
}

NUMBER_TO_CATEGORY = {v: k for k, v in CATEGORY_TO_NUMBER.items()}

RANK_TO_NUMBER = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}

NUMBER_TO_RANK = {v: k for k, v in RANK_TO_NUMBER.items()}

ALL_RANKS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
ALL_SUITS = ["c", "s", "h", "d"]
# all possible 52 cards
ALL_CARDS = [rank + suit for rank in ALL_RANKS for suit in ALL_SUITS]


def random_hand(length=5):
    random_cards = random.sample(ALL_CARDS, length)
    return sorted(random_cards, key=(lambda e: ALL_CARDS.index(e)))


_ROY_BACK = {"Street": 2,
             "Flush": 4,
             "FullHouse": 6,
             "Quads": 10,
             "StreetFlush": 15,
             "Royal": 25, }

_ROY_MID = {"Trips": 2,
            "Street": 4,
            "Flush": 8,
            "FullHouse": 12,
            "Quads": 20,
            "StreetFlush": 30,
            "Royal": 50}

_ROY_FRONT = {"Pair6": 1,
              "Pair7": 2,
              "Pair8": 3,
              "Pair9": 4,
              "PairT": 5,
              "PairJ": 6,
              "PairQ": 7,
              "PairK": 8,
              "PairA": 9,
              "Trips2": 10,
              "Trips3": 11,
              "Trips4": 12,
              "Trips5": 13,
              "Trips6": 14,
              "Trips7": 15,
              "Trips8": 16,
              "Trips9": 17,
              "TripsT": 18,
              "TripsJ": 19,
              "TripsQ": 20,
              "TripsK": 21,
              "TripsA": 22,
              }


def royalties(where, handranking):
    assert(where in ["back", "mid", "front"])
    if where in ["back", "mid"]:
        if handranking[0] == "StreetFlush":
            if handranking[1] == "A":
                final_ranking = "Royal"
            else:
                final_ranking = "StreetFlush"
        else:
            final_ranking = handranking[0]
        if where == "back":
            roy_dict = _ROY_BACK
        else:
            roy_dict = _ROY_MID
        
    else:
        if handranking[0] == "Trips":
            final_ranking = "Trips" + handranking[1]
        elif handranking[0] == "OnePair":
            final_ranking = "Pair" + handranking[1]
        else:
            final_ranking = handranking[0]
        roy_dict = _ROY_FRONT
    if roy_dict.has_key(final_ranking):
        return roy_dict[final_ranking]
    else:
        return 0


class TestRoyalties (unittest.TestCase):

    def test_back(self):
        self.assertEqual(royalties("back", ("Trips", "A", "K", "J")), 0)
        self.assertEqual(
            royalties("back", ("HighCard", "9", "8", "5", "4", "3")), 0)
        self.assertEqual(
            royalties("back", ("Flush", "A", "K", "J", "7", "4")), 4)
        self.assertEqual(royalties("back", ("StreetFlush", "A")), 25)
        self.assertEqual(royalties("back", ("StreetFlush", "6")), 15)
        self.assertEqual(royalties("back", ("StreetFlush", "J")), 15)

    def test_mid(self):
        self.assertEqual(royalties("mid", ("Trips", "A", "K", "J")), 2)
        self.assertEqual(
            royalties("mid", ("HighCard", "9", "8", "5", "4", "3")), 0)
        self.assertEqual(
            royalties("mid", ("Flush", "A", "K", "J", "7", "4")), 8)
        self.assertEqual(royalties("mid", ("StreetFlush", "A")), 50)
        self.assertEqual(royalties("mid", ("StreetFlush", "6")), 30)
        self.assertEqual(royalties("mid", ("StreetFlush", "J")), 30)

    def test_front(self):
        self.assertEqual(royalties("front", ("HighCard", "A", "K", "J")), 0)
        self.assertEqual(royalties("front", ("HighCard", "T", "5", "3")), 0)
        self.assertEqual(royalties("front", ("HighCard", "A", "Q", "J")), 0)
        self.assertEqual(royalties("front", ("OnePair", "A", "J")), 9)
        self.assertEqual(royalties("front", ("OnePair", "Q", "A")), 7)
        self.assertEqual(royalties("front", ("Trips", "Q")), 20)
        self.assertEqual(royalties("front", ("Trips", "5")), 13)
