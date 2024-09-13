from collections import defaultdict

import uvicorn
from Levenshtein import distance
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class RoundWords(BaseModel):
    words: list[str]


class RoundDuplicates(BaseModel):
    words: list[list[int]]


class WordPair(BaseModel):
    word1: str
    word2: str


@app.post("/version")
def version() -> int:
    return 1


@app.post("/v1/find_duplicates")
def find_duplicates(round_words: RoundWords) -> RoundDuplicates:
    duplicates = [[] for _ in range(len(round_words.words))]
    for i in range(len(duplicates)):
        for j in range(i + 1, len(duplicates)):
            if is_duplicates(WordPair(word1=round_words.words[i], word2=round_words.words[j])):
                duplicates[i].append(j)
                duplicates[j].append(i)
    return RoundDuplicates(words=duplicates)


@app.post("/v1/is_duplicates")
def is_duplicates(pair: WordPair) -> bool:
    word1 = normalize(pair.word1)
    word2 = normalize(pair.word2)

    if len(word1) > len(word2):
        word1, word2 = word2, word1

    if word1 == word2:
        return True

    dist = distance(word1, word2)
    # common_substring = SequenceMatcher(None, word1, word2).find_longest_match().size
    common_substring = common_size(word1, word2)

    if common_substring == len(word1) and len(word1) >= 3:
        return True

    if len(word1) <= 3:
        return dist <= 1 and common_substring >= 2

    if common_substring > 3 and common_substring / len(word1) > 0.5:
        return True

    if common_substring / len(word1) < 0.5:
        return dist < common_substring

    if len(word1) != len(word2):
        return dist / len(word2) <= 0.5 and common_substring / len(word1) >= 0.75

    return dist / len(word1) < 0.25


def common_size(word1: str, word2: str) -> int:
    result = 0
    for i in range(len(word2) - len(word1) + 1 + (1 if len(word1) > 0 else 0)):
        skipped = 0
        current = 0
        for j in range(len(word1)):
            if i + j < len(word2) and word1[j] == word2[i + j]:
                current += 1
            elif skipped < len(word1) // 5:
                skipped += 1
            else:
                break
        result = max(result, current)
    return result


def remove_repeating(word: str) -> str:
    result = ""
    prev = None
    for ch in word:
        if ch != prev:
            if prev:
                result += prev
            prev = ch
    if prev:
        result += prev
    return result


def normalize(word: str) -> str:
    mapping = {
        "-": "",
        "ё": "е",
        # "qu": "кв",
        # "sh": "ш",
        # "ch": "ч",
        # "th": "c",
        # "ph": "ф",
        # "wh": "в",
        # "ck": "к",
        # "ee": "и",
        # "oo": "у",
        # "ea": "и",
        "a": "а",
        "b": "б",
        "c": "ц",
        "d": "д",
        "e": "е",
        "f": "ф",
        "g": "г",
        "h": "х",
        "i": "и",
        "j": "ж",
        "k": "к",
        "l": "л",
        "m": "м",
        "n": "н",
        "o": "о",
        "p": "п",
        "q": "к",
        "r": "р",
        "s": "с",
        "t": "т",
        "u": "у",
        "v": "в",
        "w": "в",
        "x": "х",
        "y": "у",
        "z": "з",
    }

    # word = word.lower()
    # for en, ru in mapping.items():
    #     word = word.replace(en, ru)
    #
    # return remove_repeating(word)
    return "".join([mapping.get(ch, ch) for ch in word.lower()])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
