#compare two final 13 card hands to determine winner incl royalties. check for legal hand included


from helping_functions import hand_rank, hand_rank3, royalties_back, royalties_middle, royalties_front

def find_winner(own_front, own_middle, own_back, opp_front, opp_middle, opp_back):
    own_front_g=hand_rank3(own_front)
    own_middle_g=hand_rank(own_middle)
    own_back_g=hand_rank(own_back)
    opp_front_g=hand_rank3(opp_front)
    opp_middle_g=hand_rank(opp_middle)
    opp_back_g=hand_rank(opp_back)
    value=0

    own_front_l=[own_front_g[0]]+list(own_front_g[1])
    own_middle_l=[own_middle_g[0]]+list(own_middle_g[1])
    own_back_l=[own_back_g[0]]+list(own_back_g[1])
    if own_front_l<own_middle_l and own_middle_l<=own_back_l:
        legal_own=1
    else:
        legal_own=0
    opp_front_l=[opp_front_g[0]]+list(opp_front_g[1])
    opp_middle_l=[opp_middle_g[0]]+list(opp_middle_g[1])
    opp_back_l=[opp_back_g[0]]+list(opp_back_g[1])
    if opp_front_l<opp_middle_l and opp_middle_l<=opp_back_l:
        legal_opp=1
    else:
        legal_opp=0
    if legal_own==0 and legal_opp==0:
        value=0
    elif legal_own==1 and legal_opp==0:
        value=6+royalties_front(own_front_g)+royalties_middle(own_middle_g)+royalties_back(own_back_g)
    elif legal_own==0 and legal_opp==1:
        value=-6-royalties_front(opp_front_g)-royalties_middle(opp_middle_g)-royalties_back(opp_back_g)
    else:
        win=0
        if own_front_l==opp_front_l:
            pass
        elif own_front_l>opp_front_l:
            win=win+1
        else:
            win=win-1
        if own_middle_l==opp_middle_l:
            pass
        if own_middle_l>opp_middle_l:
            win=win+1
        else:
            win=win-1
        if own_back_l==opp_back_l:
            pass
        elif own_back_l>opp_back_l:
            win=win+1
        else:
            win=win-1
        if win==3:
            win=win+3
        if win==-3:
            win=win-3
        value=win+royalties_front(own_front_g)+royalties_middle(own_middle_g)+royalties_back(own_back_g)-royalties_front(opp_front_g)-royalties_middle(opp_middle_g)-royalties_back(opp_back_g) 
       
    return value
           
            
     