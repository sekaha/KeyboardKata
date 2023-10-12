import curses
from random import choice
from time import time
from itertools import product
from math import ceil

gram_data = {}


def begin_recording():
    try:
        with open("data/data.txt", "r") as file:
            for l in file:
                new_data = l.strip("\n").split(", ")
                gram_data[new_data[0]] = [float(n) for n in new_data[1:]]
    except:
        open("data/data.txt", "w")


def remove_outliers(array):
    if len(array) > 8:
        q_i = ceil(0.25 * len(array))
        q1, q3 = array[q_i], array[-q_i]
        iqr = q3 - q1
        lb, ub = q3 - 1 * iqr, q3 + 1 * iqr

        return [v for v in array if lb < v < ub]
    else:
        return array


def output_data():
    with open("data/data.txt", "w") as file:
        for gram in gram_data.keys():
            cleaned = [str(n) for n in remove_outliers(sorted(gram_data[gram]))]
            file.write(f"{gram}, " + ", ".join(cleaned) + "\n")


def get_key_times(terminal, n):
    curses.noecho()
    terminal.addstr(
        f"Let's start typing {n}-grams! Press (esc) to save your results (it will not save otherwise dummy). Enter to start."
    )
    text = ""
    ngram = ""

    while True:
        # start, end = 0, 0
        key = terminal.getch()

        if key == 27:  # ESC ley"
            break
        elif not key == 263:  # don't consider backspace
            if not text:
                start = time()

            char = chr(key)
            text += char
            terminal.addch(char)

            if len(text) == max(n, 2):
                if text == ngram:
                    end = time()
                    ms = round((end - start) * 1000, 2)
                    gram = ngram[1:] if n == 1 else ngram
                    gram_data[gram] = gram_data.get(gram, []) + [ms]

        if len(text) == max(n, 2) or key == 10:  # enter key
            # go to next example
            ngram = "" + " " * (n == 1)
            text = ""
            # def need to weight the choice
            terminal.clear()
            chars = "qwertyuiopasdfghjkl;zxcvbnm,./"
            ngram += "".join([choice("mn") for i in range(n)])
            terminal.addstr(f"Type {ngram}\n")

        terminal.refresh()


begin_recording()

for i in range(2, 3):
    window = curses.wrapper(get_key_times, i)
output_data()


def get_avg(array):
    return sum(map(float, array)) / len(array)


def get_key_data(chars):
    def get_median(array):
        return float(array[len(array) // 2])

    def get_avg(array):
        return sum(map(float, array)) / len(array)

    return int(sum([get_avg(gram_data.get(c, ["0"])) for c in chars]) / len(chars))


def ngram_speed(ngram):
    def get_median(array):
        return float(array[len(array) // 2])

    return get_avg(gram_data.get(ngram, ["0"]))  # + get_key_data(trigram[0])


def print_data():
    baseline = get_key_data("asdfjkl;")
    # print("baseline", baseline)
    # print("gh", get_key_data("gh") - baseline)
    # print("top no lateral", get_key_data("qweruiop") - baseline)
    # print("center no lateral", get_key_data("asfdjkl;") - baseline)
    # print("center", get_key_data("asfdghjkl;") - baseline)
    # print("top", get_key_data("qwertyuiopt") - baseline)
    # print("bottom", get_key_data("zxcvm,./vb") - baseline)
    # print("left", get_key_data("qwerasfzxvctgb") - baseline)
    # print("right", get_key_data("uiopjlk;m,./yhn") - baseline)

    # finger strengths
    l_pinky = get_avg([ngram_speed("".join(t)) for t in product("qaz", repeat=2)]) - (
        ngram_speed("aa")
    )
    l_ring = get_avg([ngram_speed("".join(t)) for t in product("wsx", repeat=2)]) - (
        ngram_speed("ss")
    )
    l_middle = get_avg([ngram_speed("".join(t)) for t in product("edc", repeat=2)]) - (
        ngram_speed("dd")
    )
    l_index = get_avg([ngram_speed("".join(t)) for t in product("rfv", repeat=2)]) - (
        ngram_speed("ff")
    )

    print("left pinky", l_pinky)
    print("left ring", l_ring)
    print("left middle", l_middle)
    print("left index", l_index)

    r_pinky = get_avg([ngram_speed("".join(t)) for t in product("p;/", repeat=2)]) - (
        ngram_speed(";;")
    )
    r_ring = get_avg([ngram_speed("".join(t)) for t in product("ol.", repeat=2)]) - (
        ngram_speed("ll")
    )
    r_middle = get_avg([ngram_speed("".join(t)) for t in product("ik,", repeat=2)]) - (
        ngram_speed("kk")
    )
    r_index = get_avg([ngram_speed("".join(t)) for t in product("ujm", repeat=2)]) - (
        ngram_speed("jj")
    )

    print("right pinky", r_pinky)
    print("right ring", r_ring)
    print("right middle", r_middle)
    print("right index", r_index)

    print("------------")

    baseline = (r_index + l_index) // 2

    print("pinky", ((r_pinky + l_pinky) // 2) / baseline)
    print("ring", ((r_ring + l_ring) // 2) / baseline)
    print("middle", ((r_middle + l_middle) // 2) / baseline)
    print("index", ((r_index + l_index) // 2) / baseline)

    print("------------ratios")

    pinky_rat = l_pinky / r_pinky
    ring_rat = l_ring / r_ring
    middle_rat = l_middle / r_middle
    index_rat = l_index / r_index

    print("pinky", pinky_rat)
    print("ring", ring_rat)
    print("middle", middle_rat)
    print("index", index_rat)

    print("cumm ratio", (pinky_rat + ring_rat + index_rat + middle_rat) / 4)

    print("---------- unigrams ----------")
    print("left index", get_key_data("rfv"))
    print("left middle", get_key_data("edc"))
    print("left ring", get_key_data("wsx"))
    print("left pinky", get_key_data("qaz"))

    print("---------- sft ----------")
    print("aaa", ngram_speed("aaa"))
    print("sss", ngram_speed("sss"))
    print("ddd", ngram_speed("ddd"))
    print("fff", ngram_speed("fff"))

    print("---------- speed v.s. distance ----------")
    print("jh 1.00", ngram_speed("jh"))
    print("ny 2.14", ngram_speed("ny"))
    print("my 2.66", ngram_speed("mu"))

    print("---------- rolls ----------")
    print("mn", ngram_speed("nm") - ngram_speed("mn"))
    print("jh", ngram_speed("hj") - ngram_speed("jh"))
    print("uy", ngram_speed("uy") - ngram_speed("yu"))


print_data()
