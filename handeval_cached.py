
import itertools
import math

from handeval_naive import handnumber_5card, handnumber_3card

# test via 4 out of 20
def comb_classic(k_choosen, n_total):
    """Classic mathematical combinatorial forumula
    choose k out of a total n without order without replacement"""
    assert(isinstance(k_choosen, int))
    assert(isinstance(n_total, int))
    assert(0 <= k_choosen <= n_total)
    nom = math.factorial(n_total)
    denom = math.factorial(n_total - k_choosen) * math.factorial(k_choosen)
    assert(nom % denom == 0)
    return int(nom // denom)


def comb(k_choosen, n_total):
    """more efficient comb_classic"""
    assert(isinstance(k_choosen, int))
    assert(isinstance(n_total, int))
    assert(0 <= k_choosen <= n_total)
    if k_choosen == 0 or k_choosen == n_total:
        return 1
    if k_choosen == 1 or k_choosen == (n_total - 1):
        return n_total
    nom = n_total
    for c in range(n_total - 1, k_choosen - 1, -1):
        print(c)
        nom *= c
    denom = 1
    for c in range(2, k_choosen + 1):
        denom *= c
   # print("{0} / {1}".format(nom, denom))
    assert(nom % denom == 0)
    return nom // denom
