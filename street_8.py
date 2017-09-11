#optimal 8th-street play. due to inefficient algorithm time needed >10min (for a fairly simple problem).
#need to be smarter

import itertools
from street_9 import street_9


cards_dealt=['Jh', 'Qc', '8d' ]
dead_cards=['Th', 'Jd']
own_front=['Qd', '2s' ]
own_middle=['As', 'Kc', 'Ac', '8h']
own_back=['9c', '5c','6c']
opp_front=['Ah', 'Ad', '2d']
opp_middle=['3c', 'Td', 'Ts', '3h']
opp_back=['4c', '4h', '4s', 'Jc']


#def street_8(cards_dealt, dead_cards, own_front, own_middle, own_back, opp_front, opp_middle, opp_back):

check_for_dupl=cards_dealt+ dead_cards+ own_front+ own_middle+ own_back+ opp_front+ opp_middle+ opp_back
if len(check_for_dupl)!=len(set(check_for_dupl)):
    print('duplicates in street 9')
if len(check_for_dupl)!=25:
    print('not 25 cards in street 9')
list_of_perm=list(itertools.permutations(cards_dealt))
list_of_perm1=[]
list_of_perm2=[]
for i in range(6):
    list_of_perm[i]=list_of_perm[i][:-1]
    list_of_perm[i]=list(list_of_perm[i])
    list_of_perm[i].append([])
    list_of_perm[i].append([])
    x=list(itertools.permutations(list_of_perm[i]))
    for j in x:
        list_of_perm1.append(j)
for i in list_of_perm1:
    if i not in list_of_perm2:
        list_of_perm2.append(i)
deck=([r+s for r in '23456789TJQKA' for s in 'shdc'])
remaining_cards=([x for x in deck if x not in check_for_dupl])
list_of_poss=list(itertools.combinations(remaining_cards, 3)) 
value=[]
list_of_perm3=[]
for i in range(len(list_of_perm2)):
    perm=list(list_of_perm2[i])
    own_fronti=own_front[:]
    own_middlei=own_middle[:]
    own_backi=own_back[:]
    opp_fronti=opp_front[:]
    opp_middlei=opp_middle[:]
    opp_backi=opp_back[:]
    while len(own_fronti)<2.5:
        own_fronti.append(perm[0])
        perm.remove(perm[0])
    while len(own_middlei)<4.5:
        own_middlei.append(perm[0])
        perm.remove(perm[0])
    while len(own_backi)<4.5:
        own_backi.append(perm[0])
        perm.remove(perm[0])
    list_of_perm3.append([own_fronti, own_middlei, own_backi])
def remove_empty(l):
    return list(filter(lambda x:not isinstance(x, (str, list, tuple)) or x, (remove_empty(x) if isinstance(x, (tuple, list)) else x for x in l)))
list_of_perm4=[]
list_of_perm4=remove_empty(list_of_perm3)
list_of_perm5=[]
for i in list_of_perm4:
    if i not in list_of_perm5:
        list_of_perm5.append(i)
print(list_of_perm5) 

        

for i in range(len(list_of_perm5)):
    valuee=0
    for j in range(len(list_of_poss)):
        [x,y]=street_9(list(list_of_poss[j]), dead_cards, opp_front, opp_middle, opp_back, list_of_perm5[i][0],list_of_perm5[i][1], list_of_perm5[i][2])
        valuee=valuee-x
        print(i,j, 'i,j')
    z=valuee/len(list_of_poss)
    value.append(z)
print(value)
value_of_best=max(value)
best_comb=list_of_perm[value.index(value_of_best)]
#return value_of_best, best_comb

