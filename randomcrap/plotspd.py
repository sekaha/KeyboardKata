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

offset = min([get_avg(gram_data[c+c]) for c in ltrs])

key_combos = sum(
    [[ltrs[i] + ltrs[j] for j in range(i, len(ltrs)) if ltrs[i] != ltrs[j]] for i in range(len(ltrs))], []
)

print(key_combos)

dist_to_times = {}

for bg in key_combos:
    dist = pen.get_bigram_penalties("".join(bg))[6]
    bg_times = gram_data["".join(bg)]

    if bg[1] != bg[0]:
        bg_times += gram_data["".join(reversed(bg))]

    dist_to_times[dist] = dist_to_times.get(dist,[])+bg_times

dists = [(d) for d in dist_to_times.keys()]
times = [get_avg(dist_to_times[d])-offset for d in dist_to_times.keys()] 


#dists = [(pen.get_bigram_penalties("".join(bg))[6]) for bg in key_combos]
#times = [
#    get_avg(gram_data["".join(bg)] + gram_data["".join(reversed(bg))]) - offset
#    for bg in key_combos
#]

plt.scatter(dists, times, label="Time to Type by Bigram Distance")

# putting labels
plt.xlabel("Distance")
plt.ylabel("Time to Type (ms)")

# Regress line:
slope, intercept, r_value, p_value, std_err = stats.linregress([log2(d) for d in dists], times)
#
#print("slope", slope, "intercept", intercept)
x = np.arange(1,2.66,0.05)
regression_line = slope * np.log2(x) + intercept

#plt.plot(x, regression_line, color='blue', label='Regression Line')

print("stderr",r_value)


slope, intercept, r_value, p_value, std_err = stats.linregress(dists, times)
regression_line = slope * np.array(dists) + intercept
#plt.plot(dists, regression_line, color='red', label='Regression Line')

print("offset", offset)

regression_line = 15.86750971186548 * np.array(dists) + (117.50531805429226-offset)
plt.plot(dists, regression_line, color='red', label='Regression Line')

print("stderr",r_value)

#for i, bg in enumerate(key_combos):
#    plt.annotate(bg, (dists[i], times[i]))

# function to show plot
plt.show()
