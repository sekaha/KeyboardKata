import pandas as pd
from keyboard import Keyboard


class Corpus:
    def __init__(self, file, valid=Keyboard()):
        if isinstance(file, str):
            data = pd.read_csv(file, sep="\t", header=None, names=["chars", "freq"])
        else:
            data = pd.DataFrame(file, columns=["chars", "freq"])

        # making characters lowercase and normalizing special chars
        translation = str.maketrans('§~!@#$%^&*()_+{}|:"<>?', " `1234567890-=[]\;',./")
        data["chars"] = data["chars"].str.translate(translation).str.lower()

        # merge data now tha it has been normalized
        data = data.groupby("chars")["freq"].sum().reset_index()

        # removing invalid rows
        valid_k = "".join(["".join(row) for row in valid.kb])  # + " \n"
        data = data[data["chars"].apply(lambda s: all(c in valid_k for c in s))]
        data = data[data["freq"] > 0]  # remove all non-used bigraphs or trigraphs

        # sorting the data from least frequent to most frequent
        self.data = data.sort_values(
            by=data.columns[1], ignore_index=True, ascending=False
        )
