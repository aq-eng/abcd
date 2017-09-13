
import unittest
import random
import time

from definitions import (ALL_SUITS, ALL_RANKS, ALL_CARDS,
                         RANK_TO_NUMBER, NUMBER_TO_RANK,
                         CATEGORY_TO_NUMBER, NUMBER_TO_CATEGORY,
                         random_hand)


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
        return ("StreetFlush", cardset[0][0])
    groups = grouptuple(cardset)
    if groups[0][0] == 4:
        return ("Quads", groups[0][1], groups[1][1])
    if groups[0][0] == 3 and groups[1][0] == 2:
        return ("FullHouse", groups[0][1], groups[1][1])
    if is_fl:
        return ("Flush",) + tuple([e[0] for e in cardset])
    if is_str:
        return ("Street", cardset[0][0])
    if groups[0][0] == 3:
        return ("Trips", groups[0][1], groups[1][1], groups[2][1])
    if groups[0][0] == 2 and groups[1][0] == 2:
        return ("TwoPair", groups[0][1], groups[1][1], groups[2][1])
    if groups[0][0] == 2:
        return ("OnePair", groups[0][1], groups[1][1], groups[2][1], groups[3][1])
    return ("HighCard",) + tuple([e[0] for e in cardset])


def handnumber_5card(cardset):
    return handranking_to_handnumber(handranking_5card(cardset))

class Test5Card (unittest.TestCase):

    def test_yesquads(self):
        self.assertEqual(handranking_5card(["Ac", "As", "Ad", "Ah", "9c"]),
                         ("Quads", "A", "9",))
        self.assertEqual(handranking_5card(["Ac", "9s", "9d", "9h", "9c"]),
                         ("Quads", "9", "A",))
        self.assertEqual(handranking_5card(["7c", "7s", "7d", "7h", "4c"]),
                         ("Quads", "7", "4",))

    def test_yesfullhouse(self):
        self.assertEqual(handranking_5card(["Ac", "As", "Ad", "Kh", "Kc"]),
                         ("FullHouse", "A", "K",))
        self.assertEqual(handranking_5card(["Ac", "As", "4d", "4h", "4c"]),
                         ("FullHouse", "4", "A",))
        self.assertEqual(handranking_5card(["Jc", "Jh", "Jd", "8h", "8c"]),
                         ("FullHouse", "J", "8",))

    def test_yestrips(self):
        self.assertEqual(handranking_5card(["Ac", "7s", "7d", "7h", "4c"]),
                         ("Trips", "7", "A", "4",))
        self.assertEqual(handranking_5card(["Ac", "As", "Ad", "Jh", "4c"]),
                         ("Trips", "A", "J", "4",))
        self.assertEqual(handranking_5card(["Ac", "Jh", "8d", "8h", "8c"]),
                         ("Trips", "8", "A", "J",))

    def test_yestwopair(self):
        self.assertEqual(handranking_5card(["Ac", "As", "7d", "7h", "4c"]),
                         ("TwoPair", "A", "7", "4",))
        self.assertEqual(handranking_5card(["Ac", "Ks", "Kc", "4h", "4c"]),
                         ("TwoPair", "K", "4", "A",))
        self.assertEqual(handranking_5card(["Ac", "Jh", "Jd", "8h", "8c"]),
                         ("TwoPair", "J", "8", "A",))
        self.assertEqual(handranking_5card(["Ac", "Ah", "Jd", "8h", "8c"]),
                         ("TwoPair", "A", "8", "J",))

    def test_yesonepair(self):
        self.assertEqual(handranking_5card(["Ac", "As", "7d", "5h", "4c"]),
                         ("OnePair", "A", "7", "5", "4",))
        self.assertEqual(handranking_5card(["Ac", "Ks", "Kc", "Th", "4c"]),
                         ("OnePair", "K", "A", "T", "4",))
        self.assertEqual(handranking_5card(["Ac", "Jh", "Jd", "4h", "2c"]),
                         ("OnePair", "J", "A", "4", "2",))
        self.assertEqual(handranking_5card(["Kc", "Qh", "Jd", "8h", "8c"]),
                         ("OnePair", "8", "K", "Q", "J",))

    def test_yeshigh(self):
        self.assertEqual(handranking_5card(["Ac", "Ks", "7d", "5h", "4c"]),
                         ("HighCard", "A", "K", "7", "5", "4",))
        self.assertEqual(handranking_5card(["Ac", "Ks", "Qc", "Th", "4c"]),
                         ("HighCard", "A", "K", "Q", "T", "4",))
        self.assertEqual(handranking_5card(["7c", "6h", "4d", "3h", "2c"]),
                         ("HighCard", "7", "6", "4", "3", "2",))
        self.assertEqual(handranking_5card(["Kc", "Qh", "Jd", "8h", "4c"]),
                         ("HighCard", "K", "Q", "J", "8", "4",))


def handranking_3card(cardset):
    assert(len(cardset) == 3)
    for e in cardset:
        assert(e in ALL_CARDS)
    groups = grouptuple(cardset)
    if groups[0][0] == 3:
        return ("Trips", groups[0][1])
    if groups[0][0] == 2:
        return ("OnePair", groups[0][1], groups[1][1], )
    return ("HighCard",) + tuple([e[0] for e in cardset])

def handnumber_3card(cardset):
    return handranking_to_handnumber(handranking_3card(cardset))

class Test3Card(unittest.TestCase):

    def test_yestrips(self):
        self.assertEqual(handranking_3card(["Kc", "Kh", "Kd"]),
                         ("Trips", "K",))


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


class TestHandConversion(unittest.TestCase):

    def test_rankconvert(self):
        for test_len in [3, 5]:
            for e in range(1000):
                test_hand = random_hand(test_len)
                if test_len == 5:
                    test_ranking = handranking_5card(test_hand)
                else:
                    test_ranking = handranking_3card(test_hand)
                forward_convert = handranking_to_handnumber(test_ranking)
                back_convert = handnumber_to_handranking(forward_convert)
                self.assertEqual(test_ranking, back_convert)


def benchmark(handlen=5):
    to_be_tested = []
    for test_iteration in range(10000):
        to_be_tested.append(random_hand(handlen))
    starttime = time.time()
    evalfunc = handnumber_5card if handlen == 5 else handnumber_3card
    for test_hand in to_be_tested:
        retval = evalfunc(test_hand)
    endtime = time.time()
    return endtime - starttime 

# benchmark (3)
# => 0.0899
# benchmark (5)
# => 0.1333

# utility functions
def handranking(cardset):
    """Generalized function"""
    if len(cardset) == 5:
        return handranking_5card(cardset)
    elif len(cardset) == 3:
        return handranking_3card(cardset)
    else:
        raise AssertionError("handranking needs 3 or 5 cards")

def handnumber(cardset):
    return handranking_to_handnumber(handranking(cardset))
    
