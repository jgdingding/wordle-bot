import string
from pprint import pprint

f = open("valid_words.txt", "r")
commons = open("commons2.txt", "r")


def satisfies_constraint(w, inw, t, exc):
    c = w
    for idx, letter in enumerate(t):
        if letter != "_" and w[idx] != letter:
            return False
        c = c.replace(letter, "", 1)
    for letter in inw:
        if letter not in c:
            return False
        c = c.replace(letter, "", 1)
    for idx, ex in enumerate(exc):
        for letter in ex:
            if w[idx] == letter:
                return False
    return True


letters = "eariotnslcudpmhgbfywkvxzjq"[::-1]
weighted = {
    "e": 11.2,
    "a": 8.5,
    "r": 7.6,
    "i": 7.5,
    "o": 7.2,
    "t": 7,
    "n": 6.7,
    "s": 5.7,
    "l": 5.5,
    "c": 4.5,
    "u": 3.6,
    "d": 3.4,
    "p": 3.2,
    "m": 3.0,
    "h": 3.0,
    "g": 2.5,
    "b": 2.1,
    "f": 1.8,
    "y": 1.8,
    "w": 1.3,
    "k": 1.1,
    "v": 1.0,
    "x": 0.3,
    "z": 0.3,
    "j": 0.2,
    "q": 0.2,
}
good_words = [w.strip() for w in commons.readlines()]


def heuristic(w):
    freq = 0
    for l in w:
        freq += weighted[l]
    count = len(set(list(w)))

    if w in good_words:
        freq += 15

    if count == 4:
        count += 0.2

    return round(freq * count)


valids = string.ascii_lowercase
inword = ""
template = ["_"] * 5
excludes = ["", "", "", "", ""]

words = f.readlines()

for i in range(6):
    guess = input("Guess: ")
    result = input("Result: ")  # ...gy.

    matches = {}

    for idx, letter in enumerate(result):
        if letter == ".":
            valids = valids.replace(guess[idx], "")
    for idx, letter in enumerate(result):
        if letter == "g":
            template[idx] = guess[idx]
            if guess[idx] not in valids:
                valids += guess[idx]
        elif letter == "y":
            if guess[idx] in matches:
                matches[guess[idx]] += 1
            else:
                matches[guess[idx]] = 1
            excludes[idx] += guess[idx]
            if guess[idx] not in valids:
                valids += guess[idx]
    for letter in inword:
        if letter not in matches:
            inword = inword.replace(letter, "")
    for let, ct in matches.items():
        if ct > inword.count(let):
            inword += let * (ct - inword.count(let))

    print(valids, inword, template, excludes)

    print("Possible Words: ")

    good_guesses = []

    for word in words:
        word = word.strip().lower()
        if len(word) != 5:
            continue

        if satisfies_constraint(word, inword, template, excludes):
            q = False
            for letter in word:
                if letter not in valids:
                    q = True
            if q:
                continue
            good_guesses.append((word, heuristic(word)))
    pprint(sorted(good_guesses, key=lambda x: x[1], reverse=True)[:10])

    print("\n" * 2 + "*" * 40)

commons.close()
f.close()
