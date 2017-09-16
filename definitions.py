
from __future__ import print_function

import random
import unittest
import time

ALL_RANKS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
ALL_SUITS = ["c", "s", "h", "d"]
# all possible 52 cards
ALL_CARDS = [rank + suit for rank in ALL_RANKS for suit in ALL_SUITS]

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

def random_hand(length=5):
    random_cards = random.sample(ALL_CARDS, length)
    return sorted(random_cards, key=(lambda e: ALL_CARDS.index(e)))

class Ranking(object):
    # __slots__ = ["rank", "cards"]

    def __init__ (self,nt=None, st=None, i32=None):
        """Creates a Ranking via nt numbered tuple, st string tuple, i32 single number"""
        if nt and st is None and i32 is None:
            self.rank = nt
        elif st and nt is None and i32 is None:
            self.rank = self.convert_st_to_nt(st)
        elif i32 and st is None and nt is None:
            self.rank = self.convert_i32_to_nt(i32)
        else:
            raise AssertionError("Ranking init must be either nt or st or i32")

    @staticmethod
    def convert_st_to_nt(st):
        if len(st) < 2:
            raise ValueError("convert_st_to_nt: {0} is too short".format(st))
        try:
            category = CATEGORY_TO_NUMBER[st[0]]
            kicker = [RANK_TO_NUMBER[e] for e in st[1:]]
        except KeyError:
            raise ValueError ("convert_st_to_nt: {0}".format(st))
        return tuple([category] + kicker)

    @staticmethod
    def convert_nt_to_st(nt):
        try:
            category = NUMBER_TO_CATEGORY[nt[0]]
            kicker = [NUMBER_TO_RANK[e] for e in nt[1:]]
        except KeyError:
            raise ValueError ("convert_nt_to_st: {0}".format(nt))
        return tuple([category] + kicker)

    def convert_i32_to_nt(i32):
        pass

    def __repr__(self):
        st = Ranking.convert_nt_to_st(self.rank)
        return "<R {0} {1}>".format(st[0], ".".join(st[1:]))

    __str__ = __repr__

    def __eq__(self, other):
        if isinstance(other, Ranking):
            return self.rank == other.rank
        else:
            raise ValueError("Ranking can only eq with other Ranking")

    def __ne__(self, other):
        return not self.__eq__(other)



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

def _helperlist_ranking_to_rankint32(inp):
    fill_list = inp + (None,) * (6 - len(inp))
    number_list = [CATEGORY_TO_NUMBER[fill_list[0]]]
    for e in fill_list[1:]:
        if e:
            number_list.append(RANK_TO_NUMBER[e])
        else:
            number_list.append(0)
    mult_list = []
    for i, num in enumerate(number_list):
        mult_list.append(16**(5 - i) * num)
    return number_list, mult_list,


def handranking_to_handnumber(inp):
    return sum(_helperlist_ranking_to_rankint32(inp)[1])


def _helperlist_ranknr_to_ranking(inp):
    divlist = map((lambda e: 16**e), range(5, -1, -1))  # constant
    retlist = []
    rest = inp
    for e in divlist:
        retlist.append(rest // e)
        rest = rest % e
    return divlist, retlist,


def handnumber_to_handranking(inp):
    _, catlist = _helperlist_ranknr_to_ranking(inp)
    category = NUMBER_TO_CATEGORY[catlist[0]]
    other = []
    for e in catlist[1:]:
        if e == 0:
            break
        else:
            other.append(NUMBER_TO_RANK[e])
    return (category,) + tuple(other)

def random_handranking():
    return Ranking.from_st(handeval_naive.handranking(random_hand(5)))

# class TestHandConversion(unittest.TestCase):

#     def test_rankconvert(self):
#         for test_len in [3, 5]:
#             for e in range(1000):
#                 test_hand = random_hand(test_len)
#                 if test_len == 5:
#                     test_ranking = handranking_5card(test_hand)
#                 else:
#                     test_ranking = handranking_3card(test_hand)
#                 forward_convert = handranking_to_handnumber(test_ranking)
#                 back_convert = handnumber_to_handranking(forward_convert)
#                 self.assertEqual(test_ranking, back_convert)

