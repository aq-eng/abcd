
import unittest
import time
import sys

import handeval_naive
import handeval_i
import handeval_pre
from definitions import random_hand, Ranking

class Test5Card (unittest.TestCase):

    def helper_eval(self, cardset, rank_st):
        calculated = handeval_i.handranking(cardset)
        expected = Ranking(st=rank_st)
        self.assertEqual(calculated, expected)

    def test_yesquads(self):
        self.helper_eval(["Ac", "As", "Ad", "Ah", "9c"], 
                         ("Quads", "A", "9"))
        self.helper_eval(["Ac", "9s", "9d", "9h", "9c"],
                         ("Quads", "9", "A",))
        self.helper_eval(["7c", "7s", "7d", "7h", "4c"],
                         ("Quads", "7", "4",))

    def test_yesfullhouse(self):
        self.helper_eval(["Ac", "As", "Ad", "Kh", "Kc"],
                         ("FullHouse", "A", "K",))
        self.helper_eval(["Ac", "As", "4d", "4h", "4c"],
                         ("FullHouse", "4", "A",))
        self.helper_eval(["Jc", "Jh", "Jd", "8h", "8c"],
                         ("FullHouse", "J", "8",))

    def test_street(self):
        self.helper_eval(["Ac", "5s", "4d", "3h", "2c"],
                         ("Street", "5"))
        self.helper_eval(["Ac", "Ks", "Qd", "Jh", "Tc"],
                         ("Street", "A"))
        self.helper_eval(["Jh", "Td", "9h", "8c", "7s"],
                         ("Street", "J"))
        self.helper_eval(["Jh", "Td", "9h", "7c", "6s"],
                         ("HighCard", "J", "T", "9", "7", "6"))
        self.helper_eval(["Qh", "Td", "9h", "8c", "7s"],
                         ("HighCard", "Q", "T", "9", "8", "7"))


    def test_yestrips(self):
        self.helper_eval(["Ac", "7s", "7d", "7h", "4c"],
                         ("Trips", "7", "A", "4",))
        self.helper_eval(["Ac", "As", "Ad", "Jh", "4c"],
                         ("Trips", "A", "J", "4",))
        self.helper_eval(["Ac", "Jh", "8d", "8h", "8c"],
                         ("Trips", "8", "A", "J",))

    def test_yestwopair(self):
        self.helper_eval(["Ac", "As", "7d", "7h", "4c"],
                         ("TwoPair", "A", "7", "4",))
        self.helper_eval(["Ac", "Ks", "Kc", "4h", "4c"],
                         ("TwoPair", "K", "4", "A",))
        self.helper_eval(["Ac", "Jh", "Jd", "8h", "8c"],
                         ("TwoPair", "J", "8", "A",))
        self.helper_eval(["Ac", "Ah", "Jd", "8h", "8c"],
                         ("TwoPair", "A", "8", "J",))

    def test_yesonepair(self):
        self.helper_eval(["Ac", "As", "7d", "5h", "4c"],
                         ("OnePair", "A", "7", "5", "4",))
        self.helper_eval(["Ac", "Ks", "Kc", "Th", "4c"],
                         ("OnePair", "K", "A", "T", "4",))
        self.helper_eval(["Ac", "Jh", "Jd", "4h", "2c"],
                         ("OnePair", "J", "A", "4", "2",))
        self.helper_eval(["Kc", "Qh", "Jd", "8h", "8c"],
                         ("OnePair", "8", "K", "Q", "J",))

    def test_yeshigh(self):
        self.helper_eval(["Ac", "Ks", "7d", "5h", "4c"],
                         ("HighCard", "A", "K", "7", "5", "4",))
        self.helper_eval(["Ac", "Ks", "Qc", "Th", "4c"],
                         ("HighCard", "A", "K", "Q", "T", "4",))
        self.helper_eval(["7c", "6h", "4d", "3h", "2c"],
                         ("HighCard", "7", "6", "4", "3", "2",))
        self.helper_eval(["Kc", "Qh", "Jd", "8h", "4c"],
                         ("HighCard", "K", "Q", "J", "8", "4",))

    # def test_3(self):
    #     self.helper_eval(["Kc", "Kh", "Kd"],
    #                      ("Trips", "K",))
    #     self.helper_eval(["5c", "5h", "5d"],
    #                      ("Trips", "5",))
    #     self.helper_eval(["Kc", "Kh", "3d"],
    #                      ("OnePair", "K", "3"))
    #     self.helper_eval(["Ac", "Ah", "6d"],
    #                      ("OnePair", "A", "6"))
    #     self.helper_eval(["Kc", "Qh", "Qd"],
    #                      ("OnePair", "Q", "K"))
    #     self.helper_eval(["Kc", "7h", "4d"],
    #                      ("HighCard", "K", "7", "4"))


def compare(times=1000):
    for e in range(times):
        rh = random_hand(5)
        ci = handeval_i.handranking(rh)
        cn = handeval_naive.handranking(rh)
        cp = handeval_pre.handranking(rh)
        if ci != cn:
            print (rh, ci.rank, cn.rank)
            sys.stdout.flush()
        if ci != cp:
            print (rh, ci.rank, cp.rank)
            sys.stdout.flush()

def benchmark(handlen=5):
    to_be_tested = []
    for test_iteration in range(100000):
        to_be_tested.append(random_hand(handlen))
    starttime = time.time()
    evalfunc = handeval_i.handranking
    for test_hand in to_be_tested:
        retval = evalfunc(test_hand)
    endtime = time.time()
    return endtime - starttime 

# latest benchmark
# naive => 1.12
# pre => 1.25
# i => 1.22
