from math import exp
from random import random


def get_keyboard_fitness(kb):
    pass


def find_optima(iterations, cooling_rate=0.95):
    initial_fitness = 999999  # change to normal qwerty fitness
    temp = 1.0  # for randomness
    cur_e = float("inf")

    for _ in range(iterations):
        # energy calculations
        new_e = float("inf")
        delta_e = new_e - cur_e

        if delta_e < 0 or random < exp(-delta_e / temp):
            # accept new keyboard
            cur_e = new_e

            pass

        tempature *= cooling_rate
