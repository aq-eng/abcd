#play street 10 optimally. test all 6 possible combinations of finishing the hand and test against opponents.
#return value and best way to assign the two cards.



import itertools
from find_winner import find_winner


"""def deal(numhands, n=5, deck=[r+s for r in '23456789TJQKA' for s in 'SHDC']):
    "Shuffle the deck and deal out numhands n-card hands."
    random.shuffle(deck)
    return [deck[hand:hand+n] for hand in range(0, n*numhands, n)]

a=deal(1)
print(a)
b=hand_rank(a[0])
print(b)"""


def street_10(cards_dealt, own_front, own_middle, own_back, opp_front, opp_middle, opp_back):
    check_for_dupl=cards_dealt+ own_front+ own_middle+ own_back+ opp_front+ opp_middle+ opp_back
    if len(check_for_dupl)!=len(set(check_for_dupl)):
        print('not ok')
    if len(check_for_dupl)!=27:
        print('not ok')
    list_of_perm=list(itertools.permutations(cards_dealt)) 
    value=[]
    for i in range(6):
        perm=list(list_of_perm[i])
        own_fronti=own_front[:]
        own_middlei=own_middle[:]
        own_backi=own_back[:]
        while len(own_fronti)<2.5:
            own_fronti.append(perm[0])
            perm.remove(perm[0])
        while len(own_middlei)<4.5:
            own_middlei.append(perm[0])
            perm.remove(perm[0])
        while len(own_backi)<4.5:
            own_backi.append(perm[0])
            perm.remove(perm[0])
        value.append(find_winner(own_fronti, own_middlei, own_backi, opp_front, opp_middle, opp_back))
    value_of_best=max(value)
    best_comb=list_of_perm[value.index(value_of_best)]
    return value_of_best, best_comb
