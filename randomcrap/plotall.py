from keyboard import *
from penalty_gen import *
import matplotlib.pyplot as plt
from itertools import product
from math import log2
from scipy import stats
import numpy as np


gram_data = {}

with open("data/data.txt", "r") as file:
    for l in file:
        new_data = l.strip("\n").split(", ")
        gram_data[new_data[0]] = [float(n) for n in new_data[1:]]

pen = Penalty()


def get_avg(array):
    return sum(array) / len(array)


ltrs = "juyhnm"
print(len(list(product(ltrs, repeat=2))))

offset = min([get_avg(gram_data[c + c]) for c in ltrs])

key_combos = sum(
    [[ltrs[i] + ltrs[j] for j in range(i, len(ltrs))] for i in range(len(ltrs))],
    [],
)


# key_combos = sum(
#    [
#        [ltrs[i] + ltrs[j] for j in range(i, len(ltrs)) if ltrs[i] != ltrs[j]]
#        for i in range(len(ltrs))
#    ],
#    [],
# )


dists = []
times = []
labels = []

for bg in key_combos:
    dist = pen.get_bigram_penalties("".join(bg))[6]

    for t in gram_data["".join(bg)]:
        dists.append(dist)
        times.append(t)
        labels.append(bg)

    for t in gram_data["".join(bg[::-1])]:
        dists.append(dist)
        times.append(t)
        labels.append(bg[::-1])


plt.scatter(dists, times)

# putting labels
# plt.ylabel("Time to Type (ms)")
# plt.xlabel("Index of Difficult (log scaling of distance in keys)")
#
## log regression
# slope, intercept, r_value, p_value, std_err = stats.linregress(
#    [log2(d + 1) for d in dists], times
# )
# x = np.arange(0, 2.66, 0.05)
#
# regression_line = slope * np.log2(x + 1) + intercept
# plt.plot(x, regression_line, color="blue", label="Regression Line")
#
# print("correlation log", r_value)
#
# linear regression

slope, intercept, r_value, p_value, std_err = stats.linregress(dists, times)
regression_line = slope * np.array(dists) + intercept
plt.plot(dists, regression_line, color="red", label="Regression Line")

print("correlation lin", r_value)

# slope2, intercept2 = 29.27922048915813, 104.25026652735144
# regression_line = slope2 * np.array(dists) + intercept2
# plt.plot(dists, regression_line, color="blue", label="Regression Line")


plt.title(f"Typing Speed by Distance (Correlation = {r_value:0.2f})")
print(slope, intercept)

for i, label in enumerate(labels):
    plt.annotate(label, (dists[i], times[i]))


# function to show plot
plt.show()
