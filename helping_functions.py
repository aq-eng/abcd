
#find the strength of a 5 card hand. Input: 5 card hand. Output: Tuple.
#Example: hand_rank(['4c', '6h', '7s', '8c', '5h'])=(4, (8, 7, 6, 5, 4))
def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    # counts is the count of each rank; ranks lists corresponding ranks
    groups = group(['--23456789TJQKA'.index(r) for r,s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1) # straight with low Ace
    straight = len(ranks) == 5 and max(ranks)-min(ranks) == 4
    flush = len(set([s for r,s in hand])) == 1
    return (9 if straight and flush and ranks == (14, 13, 12, 11, 10) else            # royal flush
            8 if straight and flush else                                              # straight flush
            7 if (4, 1) == counts else                                                # 4 of a kind
            6 if (3, 2) == counts else                                                # full house
            5 if flush else                                                           # flush
            4 if straight else                                                        # straight
            3 if (3, 1, 1) == counts else                                             # 3 of a kind
            2 if (2, 2, 1) == counts else                                             # 2 pair
            1 if (2, 1, 1, 1) == counts else                                          # pair
            0), ranks                                                                 # high card

# find strenght of 3 card hand. only 3 of a kind, pair and high possible
#example: hand_rank3(['As', '4h', 'Ad'])=(1, (14, 4))
def hand_rank3(hand):
    "Return a value indicating the ranking of a hand."
    # counts is the count of each rank; ranks lists corresponding ranks
    groups = group(['--23456789TJQKA'.index(r) for r,s in hand])
    #print('g',groups)
    counts, ranks = unzip(groups)
    return (3 if (3,) == counts else                                                  # 3 of a kind
            1 if (2, 1) == counts else                                                # pair
            0), ranks 

                                                                # high card
#helping functions
def group(items):
    "Return a list of [(count, x)...], highest count first, then highest x first."
    groups = [(items.count(item), item) for item in set(items)]
    return sorted(groups, reverse=True)       
def unzip(pairs):
    return zip(*pairs)



#find royalties of back hand. input the tuple from hand_rank, not the hand itself!
#example: royalties_back((4, (8, 7, 6, 5, 4)))=2 
def royalties_back(tuple):
    if tuple[0]==9:
        return 25
    elif tuple[0]==8:
        return 15
    elif tuple[0]==7:
        return 10
    elif tuple[0]==6:
        return 6
    elif tuple[0]==5:
        return 4
    elif tuple[0]==4:
        return 2
    else:
        return 0
    
#for middle   
def royalties_middle(tuple):
    if tuple[0]==9:
        return 50
    elif tuple[0]==8:
        return 30
    elif tuple[0]==7:
        return 20
    elif tuple[0]==6:
        return 12
    elif tuple[0]==5:
        return 8
    elif tuple[0]==4:
        return 4
    elif tuple[0]==3:
        return 2
    else:
        return 0
    
#for front, value of fantasyland can be adjusted   
def royalties_front(tuple):
    value_fl=10
    if tuple[0]==3:
        return 8+tuple[1][0]+value_fl
    elif tuple[0]==1 and tuple[1][0] :
        if tuple[1][0]>11.5:
            return tuple[1][0]-5+value_fl
        elif tuple[1][0]<11.5 and tuple[1][0]>5.5:
            return tuple[1][0]-5
        else:
            return 0
    else:
        return 0
    
#find royalties of complete 13 card hand. check for legal hand included. Input 3 hands
#example: royalties_calc(['As', 'Kc', '2h'], ['4c', '6h', '7s', '8c', '5h'],['Tc', '9h', 'Th', '9s', '9d'])=10
def royalties_calc(front, middle, back):
    tuple_front=hand_rank3(front)
    tuple_middle=hand_rank(middle)
    tuple_back=hand_rank(back)
    
    front_l=[tuple_front[0]]+list(tuple_front[1])
    middle_l=[tuple_middle[0]]+list(tuple_middle[1])
    back_l=[tuple_back[0]]+list(tuple_back[1])
    if front_l<middle_l and middle_l<=back_l:
        royalties=royalties_back(tuple_back)+royalties_middle(tuple_middle)+royalties_front(tuple_front)
        return royalties
    else:
        return 0
    
#simplify tuple, so that hands of equal strength have the same value. e.g. fluu house 2s with 4s is equal worth to 2s full of Ks
#might be necessary later for comparing hand strengths
#example: simplify_tuple((6, (12,7)))=(6, 12)   
def simplify_tuple(tuple):
    if tuple[0]==9:
        return (9, (tuple[1][0])) 
    elif tuple[0]==8:
        return (8, (tuple[1][0]))
    elif tuple[0]==7:
        return (7, (tuple[1][0]))
    elif tuple[0]==6:
        return (6, (tuple[1][0]))
    elif tuple[0]==5:
        return tuple
    elif tuple[0]==4:
        return (4, (tuple[1][0]))
    elif tuple[0]==3:
        return (3, (tuple[1][0]))
    elif tuple[0]==2:
        return tuple
    elif tuple[0]==1:
        return tuple
    elif tuple[0]==0:
        return tuple