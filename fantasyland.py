#WORK IN PROGRESS!

#solving 14, 15, 16 card fl
#idea: 1.check for sf and quads first
#      2.find all combinations of straights and flushes. add them to big_list
#      3.find best fl hand without straights and flushes
#      4.go through all elements in big_list and calculate value with subfunction two_board_hand
#      5.compare all to find max royalties
#      6.compare remaining for highest hand strength 








from helping_functions import hand_rank, hand_rank3, royalties_back, royalties_middle, royalties_front, royalties_calc, simplify_tuple
import random
import itertools

deck=[r+s for r in '23456789TJQKA' for s in 'shdc']
random.shuffle(deck)
hand=deck[:14]


#def solve_fl(hand)
big_list=[]

def hand_sort(card):
    if card[0]==('A'):
        return 14
    elif card[0]==('K'):
        return 13
    elif card[0]==('Q'):
        return 12
    elif card[0]==('J'):
        return 11
    elif card[0]==('T'):
        return 10
    else:
        return int(card[0])
    
hand_sorted=sorted(hand,key=hand_sort, reverse=True)



#add flushes
spades=[]
clubs=[]
hearts=[]
diamonds=[]
for x in hand_sorted:
    if x[1]==('s'):
        spades.append(x)
    elif x[1]==('c'):
        clubs.append(x)
    elif x[1]==('h'):
        hearts.append(x)
    elif x[1]==('d'):
        diamonds.append(x)    
print(hand_sorted)
a=list(itertools.combinations(spades, 5))
big_list.extend([list(i) for i in a])
a=list(itertools.combinations(clubs, 5))
big_list.extend([list(i) for i in a])
a=list(itertools.combinations(hearts, 5))
big_list.extend([list(i) for i in a])
a=list(itertools.combinations(diamonds, 5))
big_list.extend([list(i) for i in a])
#print(big_list)


#add straights
def check_for_straight(hand):
    straight=[]
    groups = group(['--23456789TJQKA'.index(r) for r,s in hand])
    counts, ranks = unzip(groups)
    print(ranks)
    if {14,13,12,11,10}.issubset(set(ranks)):
        straight.append(14)
    if {13,12,11,10,9}.issubset(set(ranks)):
        straight.append(13)
    if {12,11,10,9,8}.issubset(set(ranks)):
        straight.append(12)
    if {11,10,9,8,7}.issubset(set(ranks)):
        straight.append(11)
    if {10,9,8,7,6}.issubset(set(ranks)):
        straight.append(10)
    if {9,8,7,6,5}.issubset(set(ranks)):
        straight.append(9)
    if {8,7,6,5,4}.issubset(set(ranks)):
        straight.append(8)
    if {7,6,5,4,3}.issubset(set(ranks)):
        straight.append(7)
    if {6,5,4,3,2}.issubset(set(ranks)):
        straight.append(6)
    if {5,4,3,2,14}.issubset(set(ranks)):
        straight.append(5)
    return straight 
        

a=check_for_straight(hand)
print('str', a)






def group(items):
    "Return a list of [(count, x)...], highest count first, then highest x first."
    groups = [(items.count(item), item) for item in set(items)]
    return sorted(groups, reverse=True)       


def unzip(pairs):
    return zip(*pairs)

"Return a value indicating the ranking of a hand."
# counts is the count of each rank; ranks lists corresponding ranks
groups = group(['--23456789TJQKA'.index(r) for r,s in hand])
#print('g',groups)
counts, ranks = unzip(groups)
#print('c', counts)
#print('r', ranks)
if ranks == (14, 5, 4, 3, 2):
    ranks = (5, 4, 3, 2, 1) # straight with low Ace
straight = len(ranks) == 5 and max(ranks)-min(ranks) == 4
flush = len(set([s for r,s in hand])) == 1
'''print ((9 if straight and flush and ranks == (14, 13, 12, 11, 10) else            # royal flush
        8 if straight and flush else                                              # straight flush
        7 if (4, 1) == counts else                                                # 4 of a kind
        6 if (3, 2) == counts else                                                # full house
        5 if flush else                                                           # flush
        4 if straight else                                                        # straight
        3 if (3, 1, 1) == counts else                                             # 3 of a kind
        2 if (2, 2, 1) == counts else                                             # 2 pair
        1 if (2, 1, 1, 1) == counts else                                          # pair
        0), ranks )  
'''








'''



fixed_hand=['3s', '3d', '3h', '2d', '3c']
deck=[r+s for r in '23456789TJQKA' for s in 'shdc']
remaining_deck=([x for x in deck if x not in fixed_hand])
random.shuffle(remaining_deck)
new_hand=remaining_deck[:9]

def two_board_hand(new_hand, fixed_hand):
    hand_sorted=sorted(new_hand,key=hand_sort, reverse=True)
    big_list=[]
    spades=[]
    clubs=[]
    hearts=[]
    diamonds=[]
    for x in hand_sorted:
        if x[1]==('s'):
            spades.append(x)
        elif x[1]==('c'):
            clubs.append(x)
        elif x[1]==('h'):
            hearts.append(x)
        elif x[1]==('d'):
            diamonds.append(x)    
    #print(hand_sorted)
    a=list(itertools.combinations(spades, 5))
    big_list.extend([list(i) for i in a])
    a=list(itertools.combinations(clubs, 5))
    big_list.extend([list(i) for i in a])
    a=list(itertools.combinations(hearts, 5))
    big_list.extend([list(i) for i in a])
    a=list(itertools.combinations(diamonds, 5))
    big_list.extend([list(i) for i in a])
    #print(big_list)
    return(big_list)


a=two_board_hand(new_hand, fixed_hand)
print(a)

'''
        














