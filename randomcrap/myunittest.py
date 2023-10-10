import penalty_gen
from keyboard import Keyboard
from itertools import product

slope = 15.86750971186548
intercept = 117.50531805429226

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
        0: finger_pen["pinky"] * left_hand_pen,
        1: finger_pen["ring"] * left_hand_pen,
        2: finger_pen["middle"] * left_hand_pen,
        3: finger_pen["index"] * left_hand_pen,
        4: finger_pen["index"] * left_hand_pen,
        5: finger_pen["index"],
        6: finger_pen["index"],
        7: finger_pen["middle"],
        8: finger_pen["ring"],
        9: finger_pen["pinky"],
    }.get(f, 0)

    d = p[6]

    return d * slope * f_p + intercept
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

print([p for p in penalties if p[1] != round(intercept, 2)])


# trigram
# penalty_gen.get_trigram_penalties("asd")
