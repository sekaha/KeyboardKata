import concurrent.futures
from collections import Counter


def get_grams(corpus, valid=set("abcdefghijklmnopqrstuvwxyz[];',./`1234567890-= \\")):
    DATA_TYPES = {
        "characters": (1, 0),
        "bigrams": (2, 0),
        "1-skipgram": (2, 1),
        "2-skipgram": (2, 2),
        "3-skipgram": (2, 3),
        "4-skipgram": (2, 4),
        "5-skipgram": (2, 5),
        "6-skipgram": (2, 6),
        "7-skipgram": (2, 7),
    }

    unshift = str.maketrans('!@#$%^&*()_+:{}:<>|?"', "1234567890-=;[];,.\/'")
    text = open(corpus, "r").read().lower().translate(unshift)

    def create(alias, size, skip):
        grams = Counter()

        for i in range(len(text) - size - skip + 1):
            window = text[i : i + size + skip]

            # make an n-gram that skips letters between
            gram = window[: size // 2] + window[-size // 2]

            # only accept valid characters
            if all(char in valid for char in gram):
                grams[gram] += 1

        # Output a TSV file of this gram-data subtype
        with open(f"data/{alias}.txt", "w") as f:
            for chars, count in sorted(grams.items(), key=lambda x: -x[1]):
                f.write(f"{chars}\t{count}\n")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(create, alias, size, skip)
            for alias, (size, skip) in DATA_TYPES.items()
        ]
        concurrent.futures.wait(futures)


if __name__ == "__main__":
    get_grams("res/iweb-corpus-samples-cleaned.txt")
