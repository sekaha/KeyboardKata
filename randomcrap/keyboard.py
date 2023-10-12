from math import log2
from random import randint


class Keyboard:
    def __init__(
        self,
        kb=["1234567890-=", "qwertyuiop[]\\", "asdfghjkl;'", "zxcvbnm,./"],
        valid=None,
        groups=None,
    ):
        self.kb = [[c for c in row] for row in kb]
        self.finger_i = [0, 1, 2, 3, 3, 6, 6, 7, 8, 9, 9, 9, 9]
        self.row_offsets = [-0.75, -0.25, 0, 0.5]  # staggered keyboard offsets
        self.key_size = 1.9  # cm
        self.distances = {}

        # key rules
        self.groups = groups
        self.valid = set()

        # set valid to default value
        if valid == None:
            valid = "".join(kb)

        for v in valid:
            for row, keys in enumerate(self.kb):
                if v in keys:
                    self.valid.add((row, keys.index(v)))

    def __repr__(self):
        return "\n".join([" ".join(row) for row in self.kb])

    def copy(self):
        new = Keyboard()
        new.kb = [row.copy() for row in self.kb]
        new.locks = self.locks
        new.groups = self.groups
        return new

    def swap(self):
        locked = True
        group1, group2, same_group = None, None, True

        while locked:
            y1 = randint(0, len(self.kb) - 1)
            x1 = randint(0, len(self.kb[y1]) - 1)

            if self.groups:
                for group in self.groups:
                    if self.kb[y1][x1] in group:
                        group1 = group
                        break

            locked = (y1, x1) in self.locks

        locked = True

        while locked:
            y2 = randint(0, len(self.kb) - 1)
            x2 = randint(0, len(self.kb[y2]) - 1)

            if self.groups:
                for group in self.groups:
                    if self.kb[y2][x2] in group:
                        group2 = group
                        break

                if group1 and group2:
                    same_group = self.kb[y1][x1] in group2 or self.kb[y2][x2] in group1

            locked = (y2, x2) in self.locks or not same_group

        self.kb[y1][x1], self.kb[y2][x2] = self.kb[y2][x2], self.kb[y1][x1]

    # memoization of dist calculations basically :)
    def get_distance(self, x1, y1, x2, y2):
        key = (x1 - x2, y1, y2)

        if key not in self.distances:
            # shift row, vertical and horizontal distances
            dx = (x1 + self.row_offsets[y1]) - (x2 + self.row_offsets[y2])
            dy = y1 - y2

            # euclidean distance the finger moves
            dist = (dx**2 + dy**2) ** 0.5

            # https://en.wikipedia.org/wiki/Fitts%27s_law
            if self.use_fitts:
                # for now, this is inaccurate, I need to do regression analysis
                dist = log2(1 + dist)

            # adjust for genuine key size in CM
            dist *= self.key_size

            self.distances[key] = dist

        return self.distances[key]

    def get_bigram_penalty(self, start, end):
        dist_p, finger_p, sfb_p, same_hand_p = 0, 0, 0, 0
        dist_to_key2 = 0
        right_handed = 0

        if end != "\n":  # escape character for end of text and start
            # distance to key also requires knowing the push down distance
            dist_to_key2 = self.distance_down + self.distance_down
            finger_p = 1

        homerow_i = -2
        start_x, start_y = -1, homerow_i

        # Determine the coordinate location of the start and end keys
        for row_i, keys in enumerate(self.kb[::-1]):
            if start in keys:
                x1, y1 = keys.index(start), -(row_i + 1)

            if end in keys:
                x2, y2 = keys.index(end), -(row_i + 1)

        # if either key in the bigram is a space, we don't have to check for SBF, handedness will be right in the event of spaces
        left_handed = False

        if start == " " and end == " ":
            right_handed = True
        elif start == " ":
            right_handed = 6 <= self.finger_i[x2]
        elif end == " ":
            right_handed = 6 <= self.finger_i[x1]
        elif end != " " and end != "\n" and start != "\n":
            # SBF check
            sfb_p = self.finger_i[x1] == self.finger_i[x2]
            # Same hand penalty
            left_handed = (self.finger_i[x1] <= 3) and (self.finger_i[x2] <= 3)
            right_handed = (6 <= self.finger_i[x1]) and (6 <= self.finger_i[x2])

        same_hand_p = left_handed or right_handed

        # if it's an SFB you gotta move from original position instead of homerow
        if sfb_p:
            start_x, start_y = x1, y1
        else:  # return original finger to homerow and make finger two start pos homerow
            # special considerations for the spacebar key
            if start != " " and start != "\n":
                dist_to_key1 = self.get_distance(x1, y1, self.finger_i[x1], homerow_i)
                dist_to_key1 *= self.discomfort_matrix[y1][x1]
                dist_p += dist_to_key1

            if end != " " and end != "\n":
                start_x = self.finger_i[x2]

        if end != " " and end != "\n":
            # Distance to type the second key, given context of first one
            dist_to_key2 += self.get_distance(start_x, start_y, x2, y2)  # *2
            finger_p = self.discomfort_matrix[y2][x2]

        dist_to_key2 *= finger_p
        dist_p += dist_to_key2

        return dist_p, sfb_p * finger_p, same_hand_p, finger_p, right_handed
