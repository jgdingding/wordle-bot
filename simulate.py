import string
from tqdm import tqdm
import multiprocessing
from functools import partial
from copy import copy

f = open("valid_words.txt", "r")
commons = open("commons2.txt", "r")

words = f.readlines()


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

freq_table = [{} for _ in range(5)]

for word in words:
    for idx, letter in enumerate(word.strip()):
        if letter in freq_table[idx]:
            freq_table[idx][letter] += 1
        else:
            freq_table[idx][letter] = 1

for i in range(5):
    for k, v in freq_table[i].items():
        freq_table[i][k] = 100 * v / len(words)

good_words = [w.strip() for w in commons.readlines()]


def heuristic(w):
    freq = 0
    for l in w:
        # freq += letters.index(l)
        freq += weighted[l]
    cnt = len(set(list(w)))

    if w in good_words:
        freq += 15

    if cnt < 5:
        cnt += (5 - cnt) * 0.2

    h2 = 0
    for ix, l in enumerate(w):
        h2 += freq_table[ix][l]

    return round(freq * cnt) + round(h2 * 1.1)


def get_guess_string(guess, answer):
    result = list(".....")
    used = ""
    for i in range(5):
        if guess[i] == answer[i]:
            result[i] = "g"
            used += guess[i]
    for i in range(5):
        if result[i] != ".":
            continue
        if guess[i] in answer and used.count(guess[i]) + 1 <= answer.count(guess[i]):
            used += guess[i]
            result[i] = "y"
    return "".join(result)


def play(initial_guess, answer, verbose=False):
    words_copied = copy(words)
    valids = string.ascii_lowercase
    inword = ""
    template = ["_"] * 5
    excludes = ["", "", "", "", ""]

    guess = initial_guess

    guesses = [initial_guess]

    for i in range(5):
        result = get_guess_string(guess, answer)

        if result == "g" * 5:
            return i + 1

        matches = {}

        for idx, letter in enumerate(result):
            if letter == ".":
                valids = valids.replace(guess[idx], "")
                excludes[idx] += guess[idx]
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

        good_guesses = []

        for word in words_copied:
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

        if not good_guesses:
            return False
        guess = sorted(good_guesses, key=lambda x: x[1], reverse=True)[0][0]

        guesses.append(guess)

        words_copied = [x[0] for x in good_guesses]

    result = get_guess_string(guess, answer)

    if result == "g" * 5:
        return 6

    if verbose:
        print(guesses, answer)
        print(valids, inword, template, excludes)
    return False


if __name__ == "__main__":
    count = 0
    total_score = 0
    failed = 0

    p = multiprocessing.Pool(8)

    results = tqdm(p.imap(partial(play, "crane"), good_words))

    for x in results:
        if x != False:
            count += 1
            total_score += x
        else:
            failed += 1

    # for w in tqdm(good_words):
    #    count += 1
    #    score = play("crate", w)
    #    # print(w, score)
    #    if score!=False:
    #        total_score += score
    #    else:
    #        failed += 1
    #        count -= 1

    print("average score: {}".format(total_score / count))
    print("failed: {}".format(failed))


commons.close()
f.close()
