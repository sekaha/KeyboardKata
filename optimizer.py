from math import exp
from random import random
from penalty import Penalty
from keyboard import Keyboard
from corpus import clean_data


class Optimizer:
    def __init__(self, layout=Keyboard()):
        self.layout = layout
        self.penalty = Penalty()
        self.bigrams = clean_data("data/bigrams.txt", layout)

        self.skipgrams = [
            clean_data(f"data/{i}-skipgram.txt", layout) for i in range(1, 8)
        ]

        self.base_fitness = self.get_fitness(Keyboard())

    def get_fitness(self, kb):
        fitness = 0
        gram_pen = {}

        for i in self.bigrams.index:
            bg = self.bigrams["chars"][i]
            freq = self.bigrams["freq"][i]
            gram_pen[bg] = self.penalty.get_bigram_penalties(bg, kb)
            fitness += (gram_pen[bg][0]) * freq

        for i, skipgram in enumerate(self.skipgrams):
            for j in skipgram.index:
                bg = skipgram["chars"][j]
                freq = skipgram["freq"][j]
                fitness += (gram_pen[bg][0]) * freq * (1 / ((i + 1) ** 2))

        return fitness

    def find_optima(self, iterations, cooling_rate=0.999):
        best_sol, best_e = None, float("inf")

        for _ in range(5):
            # initial temp for random cooling schedule
            temp = 1.0

            # initial keyboard fitness calcs
            cur_sol = self.layout.copy()
            cur_e = 10 * (self.get_fitness(cur_sol) / self.base_fitness)
            i = 0

            for i in range(iterations):
                # make new keyboard and mutate
                new_sol = cur_sol.copy()
                new_sol.swap()

                # energy calculations
                new_e = 10 * (self.get_fitness(new_sol) / self.base_fitness)
                delta_e = new_e - cur_e

                if delta_e < 0 or random() < exp(-delta_e / temp):
                    if delta_e > 0:
                        print(exp(-delta_e / temp))
                    else:
                        print(i, round(new_e * 1000, 3), round(temp, 3))
                    print(new_sol)
                    # accept new keyboard
                    cur_sol = new_sol
                    cur_e = new_e

                if new_e < best_e:
                    best_e = new_e
                    best_sol = new_sol
                    print("new best")
                    print(round(best_e * 1000, 3))
                    print(best_sol)

                temp *= cooling_rate

        print("final best")
        print(round(best_e * 1000, 3))
        print(best_sol)

        return best_sol
