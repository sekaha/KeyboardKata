from itertools import product

# Define your set of characters
chars = "qwertyuiop[]asdfghjkl;'zxcvbmn,./"

trigrams = {"".join(tg): [0, 0, 0, 0, 0, 0, 0] for tg in list(product(chars, repeat=3))}
