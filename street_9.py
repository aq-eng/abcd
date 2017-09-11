#play street 9 optimally. test all 6 possible combinations against all of opponents possible 10th street draws, using street_10 function. 
#time needed already high



import itertools
from street_10 import street_10
from helping_functions import hand_rank, hand_rank3, royalties_back, royalties_middle, royalties_front, royalties_calc, simplify_tuple

def street_9(cards_dealt, dead_cards, own_front, own_middle, own_back, opp_front, opp_middle, opp_back):

    check_for_dupl=cards_dealt+ dead_cards+ own_front+ own_middle+ own_back+ opp_front+ opp_middle+ opp_back
    if len(check_for_dupl)!=len(set(check_for_dupl)):
        print('duplicates in street 9')
    list_of_perm=list(itertools.permutations(cards_dealt))
    deck=([r+s for r in '23456789TJQKA' for s in 'shdc'])
    remaining_cards=([x for x in deck if x not in check_for_dupl])
    list_of_poss=list(itertools.combinations(remaining_cards, 3)) 
    print(list_of_perm)
    value=[]
    big_list=[]
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
        big_list.append(list((own_fronti, own_middlei, own_backi)))
    royalties=[]
    for i in range(6):
        a=royalties_calc(big_list[i][0],big_list[i][1],big_list[i][2])
        royalties.append(a)
    max_royal=max(royalties)
    for i in range(5,-1,-1):
        if royalties[i]<max_royal:
            del big_list[i]
        else:
            pass         
    for i in range(len(big_list)):
        valuee=0    
        for j in range(len(list_of_poss)):
            [x, y]=street_10(list(list_of_poss[j]), opp_front, opp_middle, opp_back, big_list[i][0], big_list[i][1], big_list[i][2])
            valuee=valuee-x
        z=valuee/len(list_of_poss)
        value.append(z)
    value_of_best=max(value)
    best_comb=list_of_perm[value.index(value_of_best)]
    
    return value_of_best, best_comb