
from definitions import Ranking

def rank_hand(hand):
    groups = group(["--23456789TJQKA".index(r) for r,s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14,5,4,3,2):
        ranks = 5,4,3,2,1
    straight = len(ranks) == 5 and max(ranks) - min(ranks) == 4
    flush = len(set([s for r, s in hand])) == 1
    return (9 if straight and flush else
            8 if (4, 1) == counts else
            7 if (3, 2) == counts else
            6 if flush else
            5 if straight else
            4 if (3, 1, 1) == counts else
            3 if (2, 2, 1) == counts else
            2 if (2, 1, 1, 1) == counts else
            1), ranks

def group(items):
    groups = [(items.count(item), item) for item in set(items)]
    return sorted(groups, reverse=True)

def unzip(pairs):
    return zip(*pairs)

def handranking(cardset):
    cat, kickertup = rank_hand(cardset)
    tup = tuple([cat] + list(kickertup))
    # hack to remove lower street
    if cat == 9:
        return Ranking(nt=tup[:2])
    elif cat == 5:
        return Ranking(nt=tup[:2])
    else:
        return Ranking(nt=tup)
