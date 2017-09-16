from definitions import (ALL_SUITS, ALL_RANKS, ALL_CARDS,
                         RANK_TO_NUMBER, NUMBER_TO_RANK,
                         CATEGORY_TO_NUMBER, NUMBER_TO_CATEGORY,
                         random_hand)

from definitions import Ranking

import unittest


def is_flush(cardset):
    assert(len(cardset) == 5)
    suits = [e[1] for e in cardset]
    for e in suits[1:]:
        if e != suits[0]:
            return False
    return True


def is_straight(cardset):
    assert(len(cardset) == 5)
    ranks_number = [RANK_TO_NUMBER[e[0]] for e in cardset]
    if ranks_number == [14, 5, 4, 3, 2]:
        return True
    first_rank_number = ranks_number[0]
    for i, e in enumerate(ranks_number[1:]):
        if first_rank_number - i - 1 != e:
            return False
    return True


def grouptuple(inp):
    assert (len(inp) >= 1)
    res = []
    current_val = inp[0][0]
    current_len = 1
    for e in inp[1:]:
        if e[0] == current_val:
            current_len += 1
        else:
            res.append((current_len, current_val,))
            current_val = e[0]
            current_len = 1
    res.append((current_len, current_val,))
    res.sort(key=(lambda e: -e[0]))
    return res


class TestHelperFunc (unittest.TestCase):

    def test_noflush(self):
        self.assertFalse(is_flush(["Ad", "Ac", "Js", "9s", "7s"]))

    def test_yesflush(self):
        self.assertTrue(is_flush(["Ac", "Kc", "Jc", "9c", "7c"]))

    def test_nostraight(self):
        self.assertFalse(is_straight(["Js", "Tc", "9s", "8c", "4d"]))

    def test_yesstraight(self):
        self.assertTrue(is_straight(["Js", "Tc", "9s", "8c", "7d"]))

    def test_grouptuple(self):
        self.assertEqual(grouptuple(["Ac", "Ad", "Ah", "8d", "4h"]), [
                         (3, 'A'), (1, '8'), (1, '4')])
        self.assertEqual(grouptuple(["Ac", "8d", "8h", "8d", "4h"]), [
                         (3, '8'), (1, 'A'), (1, '4')])
        self.assertEqual(grouptuple(["Ac", "Ad", "Ah", "8d", "4h"]), [
                         (3, 'A'), (1, '8'), (1, '4')])


def handranking_5card(cardset):
    assert(len(cardset) == 5)
    for e in cardset:
        assert(e in ALL_CARDS)
    is_str = is_straight(cardset)
    is_fl = is_flush(cardset)
    if is_str and is_fl:
        if cardset[0][0] == "A" and cardset[1][0] == "5":
            return ("StreetFlush", "5")
        else:
            return ("StreetFlush", cardset[0][0])
    groups = grouptuple(cardset)
    if groups[0][0] == 4:
        return ("Quads", groups[0][1], groups[1][1])
    if groups[0][0] == 3 and groups[1][0] == 2:
        return ("FullHouse", groups[0][1], groups[1][1])
    if is_fl:
        return ("Flush",) + tuple([e[0] for e in cardset])
    if is_str:
        if cardset[0][0] == "A" and cardset[1][0] == "5":
            return ("Street", "5",)
        else:
            return ("Street", cardset[0][0])
    if groups[0][0] == 3:
        return ("Trips", groups[0][1], groups[1][1], groups[2][1])
    if groups[0][0] == 2 and groups[1][0] == 2:
        return ("TwoPair", groups[0][1], groups[1][1], groups[2][1])
    if groups[0][0] == 2:
        return ("OnePair", groups[0][1], groups[1][1], groups[2][1], groups[3][1])
    return ("HighCard",) + tuple([e[0] for e in cardset])


def handranking(cardset):
    return Ranking(st=handranking_5card(cardset))
