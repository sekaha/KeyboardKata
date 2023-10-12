import penalty_gen
from keyboard import Keyboard
from itertools import product

slope = 10.605790310239463
intercept = 127.15273551187612

kb = Keyboard()

# bigram tests
pen = penalty_gen.Penalty()

left_hand_pen = 1.1229625660795461

finger_pen = {
    "pinky": 1.2751677852348993,
    "ring": 1.0939597315436242,
    "middle": 0.9194630872483222,
    "index": 1.0,
}


def get_penalty(bg):
    p = pen.get_bigram_penalties(bg)
    f = p[8][0]

    f_p = {
        0: finger_pen["pinky"],
        1: finger_pen["ring"],
        2: finger_pen["middle"],
        3: finger_pen["index"],
        4: finger_pen["index"],
        5: finger_pen["index"],
        6: finger_pen["index"],
        7: finger_pen["middle"],
        8: finger_pen["ring"],
        9: finger_pen["pinky"],
    }.get(f, 0)

    d = p[6]

    return (d * slope + intercept) * f_p
    # print(f"{bg}:{d*1.9:0.1f} cm,{(d*slope*f_p+intercept) : 0.1f}", "ms")


letras = sorted("qwertuyiopasdfghjklzxcvbnm,./;")
combos = sum(
    [
        [letras[i] + letras[j] for j in range(i, len(letras))]
        for i in range(len(letras))
    ],
    [],
)

penalties = sorted([(c, round(get_penalty(c), 2)) for c in combos], key=lambda x: -x[1])

print(pen.get_bigram_penalties("yu")[6])

my_i = -1

for i, p in enumerate(penalties):
    if p[0] == "my":
        my_i = i
        break


print("\n".join([f"{a}: {b}" for (a, b) in penalties if b >= penalties[my_i][1]]))

# with open("owo.txt", "w") as f:
#    f.write(
#        "\n".join([f"{a}: {b}" for (a, b) in penalties])
#    )  # if b < round(intercept, 2)]))


# trigram
# penalty_gen.get_trigram_penalties("asd")
