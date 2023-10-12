import pandas as pd
from keyboard import Keyboard


# class Corpus:
def clean_data(file, layout=Keyboard()):
    data = pd.read_csv(file, sep="\t", header=None, names=["chars", "freq"])

    # removing invalid rows
    valid = "".join(["".join(row) for row in layout.kb])  # + " \n"
    data = data[data["chars"].apply(lambda s: all(c in valid for c in s))]

    return data
