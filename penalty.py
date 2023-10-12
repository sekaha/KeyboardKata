from keyboard import Keyboard
from math import log2

## subcategories:
# inward, outward
# skipgram/skpstroke
# scissors - neighboring fingers are used to type keys that are euclidean 2 apart or more on the board

## bistroke categories
# alt - bistroke with both hands
# roll - bistroke with one hand
# sfr(epeat) - same key twice
# sfb
# scissor moment?


class Penalty:
    def __init__(self):
        self.distances = {}

        # skipgram penalities are inverse exponential
        self.skipgram_pens = [1 / 2**i for i in range(0, 8)]
        self.finger_p = [2.7, 1.05, 0.9, 1.0]
        self.finger_p += [self.finger_p[-1]]
        self.finger_p += self.finger_p[::-1] + [self.finger_p[-1]] * 4

    # memoization of dist calculations basically :)
    def get_distance(self, x1, y1, x2, y2, layout):
        key = (abs(x1 - x2), y1, y2)

        if key not in self.distances:
            # shift row, vertical and horizontal distances
            dx = (x1 + layout.row_offsets[y1]) - (x2 + layout.row_offsets[y2])
            dy = y1 - y2

            # euclidean distance the finger moves
            dist = (dx**2 + dy**2) ** 0.5

            # Shannon formulation of fitts' law, since the speed difference should be logarithmic _in theory_
            self.distances[key] = dist  # log2(dist + 1)

        return self.distances[key]

    def get_bigram_penalties(self, bigram, layout):
        # for estimating time in seconds
        # slope = 10.605790310239463
        # intercept = 127.15273551187612

        sfb, sfr, roll, inward, outward, dist = 0, 0, 0, 0, 0, 0
        c1, c2 = tuple(bigram)

        # Determine x and y coordinates of each key
        for y, row in enumerate(layout.kb):
            if c1 in row:
                x1, y1 = row.index(c1), y

            if c2 in row:
                x2, y2 = row.index(c2), y

        # which hand it's on, 0 == left, 1 == right
        c1_hand = layout.finger_i[x1] < 6
        c2_hand = layout.finger_i[x2] < 6

        alt = c1_hand != c2_hand

        if not alt:
            # default left hand check
            inward = x1 < x2
            outward = x1 > x2

            # for right hand, swap directionality
            if not c1_hand:
                inward, outward = outward, inward

            # same finger bigram or same finger repeat check
            if layout.finger_i[x1] == layout.finger_i[x2]:
                sfr = c1 == c2
                sfb = not sfr

                if sfb:
                    dist = self.get_distance(x1, y1, x2, y2, layout)
            else:
                roll = 1

        # slope intercept to convert it milliseconds
        return dist * self.finger_p[x2], alt
        # alt, sfb, sfr, roll, inward, outward, dist, (x1, y1), (x2, y2)

    # Tristroke categories
    # alt - where you switch hands twice
    # roll - a tristoke where you switch hands once
    # onehand
    # redirect
    # sft(rigram)
    # sfr(epeat)
    # sfb (cannot be sft, must be proper sfb)
    # sfs (same finger skipgram)
    #   # sfs.trill if first and third key are the same... sfs.redirect if not
    def get_trigram_penalties(self, trigram, kb):
        alt, sfb, sfr, roll, inward, outward = False, False, False, False, False, False

        # bigram decompositions
        bg1, bg2 = trigram[:1], trigram[1:]
        bg1_pen = self.get_bigram_penalties(bg1, kb)
        bg2_pen = self.get_bigram_penalties(bg2, kb)

        # character decomposition
        c1, c2, d3 = tuple(bigram)

        alt = bg1[0] | bg2[0]
        sft = bg1[1] & bg2[1]
        sfb = bg1[1] ^ bg2[1]

        onehand = not alt
