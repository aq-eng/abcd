
import unittest
import random
import time

from definitions import ALL_CARDS, Ranking

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

SUIT_TO_NUMBER = {
    "c" : 1,
    "s" : 2,
    "h" : 3,
    "d" : 4
}

def convert(cardset):
    assert(isinstance(cardset, tuple) or isinstance(cardset, list))
    for e in cardset:
        assert(e in ALL_CARDS)
    suits = [SUIT_TO_NUMBER[e[1]] for e in cardset]
    ranks = [RANK_TO_NUMBER[e[0]] for e in cardset]
    return ranks, suits

def is_flush(suits):
    if len(suits) < 5:
        return False
    for e in suits[1:]:
        if e != suits[0]:
            return False
    return True

def is_straight(ranks):
    if len(ranks) < 5:
        return False
    if ranks == [14, 5, 4, 3, 2]:
        return True
    for i, e in enumerate(ranks[1:]):
        if ranks[0] - i - 1 != e:
            return False
    return True

def grouptuple(ranks):
    assert (len(ranks) >= 1)
    res = []
    current_val = ranks[0]
    current_len = 1
    for e in ranks[1:]:
        if e == current_val:
            current_len += 1
        else:
            res.append((current_len, current_val,))
            current_val = e
            current_len = 1
    res.append((current_len, current_val,))
    res.sort(key=(lambda e: -e[0]))
    return res

def handranking(cardset):
    assert(len(cardset) in [3, 5])
    ranks, suits = convert(cardset)
    groups = grouptuple(ranks)
    if len(cardset) == 5:
        is_str = is_straight(ranks)
        is_fl = is_flush(suits)
        if is_str and is_fl:
            if ranks == [14, 5, 4, 3, 2]:
                return Ranking(nt=(9, 5))
            else:
                return Ranking(nt=(9, ranks[0]))
        if groups[0][0] == 4:
            return Ranking(nt=(8, groups[0][1], groups[1][1]))
        if groups[0][0] == 3 and groups[1][0] == 2:
            return Ranking(nt=(7, groups[0][1], groups[1][1]))
        if is_fl:
            return Ranking(nt=(6,) + tuple(ranks))
        if is_str:
            if ranks == [14, 5, 4, 3, 2]:
                return Ranking(nt=(5, 5))
            else:
                return Ranking(nt=(5, ranks[0]))
        if groups[0][0] == 3:
            return Ranking(nt=(4, groups[0][1], groups[1][1], groups[2][1]))
        if groups[0][0] == 2 and groups[1][0] == 2:
            return Ranking(nt=(3, groups[0][1], groups[1][1], groups[2][1]))
        if groups[0][0] == 2:
            return Ranking(nt=(2, groups[0][1], groups[1][1], groups[2][1], groups[3][1]))
        return Ranking(nt=(1,) + tuple(ranks))
    else:
        if groups[0][0] == 3:
            return Ranking(nt=(4, groups[0][1]))
        if groups[0][0] == 2:
            return Ranking(nt=(2, groups[0][1], groups[1][1]))
        return Ranking(nt=(1,) + tuple(ranks))
