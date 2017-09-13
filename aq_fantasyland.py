
import itertools

from definitions import royalties, random_hand
from handeval_naive import handranking, handnumber

def candidates(cardset):
    """Checks all possible 3 and 5 card combinations for potential royalties.potential

    Runs through 4368 combinations"""
    # counter = 0
    assert(len(cardset) >= 13)
    cand_list = []
    for position, amountcards in [["back", 5], ["mid", 5], ["front", 3]]:
        for cur_cand in itertools.combinations(cardset, amountcards):
            cur_ranking = handranking(cur_cand)
            # counter += 1
            cur_roy = royalties(position, cur_ranking)
            if cur_roy > 0:
                cand_list.append((cur_cand, position, cur_roy))
    # print(counter)
    return cand_list


def expand_candidate(cardset, choosencards, choosenposition):
    """ Returns an iterator over possible (front, mid, back)"""
    remaining_cardset = []
    for e in cardset:
        if e not in choosencards:
            remaining_cardset.append(e)
    assert(len(cardset) - len(choosencards) == len(remaining_cardset))
    # start with removing a five block
    for cur_second in itertools.combinations(remaining_cardset, 5):
        final_cardset = []
        for e in remaining_cardset:
            if e not in cur_second:
                final_cardset.append(e)
        assert(len(remaining_cardset) - 5 == len(final_cardset))
        if choosenposition == "front":
            for cur_third in itertools.combinations(final_cardset, 5):
                yield (choosencards, cur_second, cur_third)
        elif choosenposition == "mid":
            for cur_third in itertools.combinations(final_cardset, 3):
                yield (cur_third, choosencards, cur_second)
        elif choosenposition == "back":
            for cur_third in itertools.combinations(final_cardset, 3):
                yield (cur_third, cur_second, choosencards)

def expand_candidates(cardset, candidate_list):
    for choosencards, position, royalties in candidate_list:
        for res in expand_candidate(cardset, choosencards, position):
            yield res    


def final_eval(backset, midset, frontset):
    br, mr, fr = handranking(backset), handranking(midset), handranking(frontset)


# Testcode
# for e in range(100):
#     print (len(candidates(random_hand(14))))
# max in 100: 270

c = random_hand(14)
a = list(expand_candidates(c, candidates(c)))
for e in a:
    final_eval(e[0], e[1], e[2])

# runs in ~2 secs
