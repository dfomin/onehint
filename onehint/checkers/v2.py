from difflib import SequenceMatcher

from Levenshtein import distance

from onehint.utils import fuzzy_common_size, remove_repeating


def is_duplicates(word1: str, word2: str) -> bool:
    word1 = normalize(word1)
    word2 = normalize(word2)

    if len(word1) > len(word2):
        word1, word2 = word2, word1

    if word1 == word2:
        return True

    dist = distance(word1, word2)
    common_substring = SequenceMatcher(None, word1, word2).find_longest_match().size
    # common_substring = fuzzy_common_size(word1, word2)

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


def normalize(word: str) -> str:
    mapping = {
        "-": "",
        "qu": "кв",
        "sh": "ш",
        "ch": "ч",
        "th": "c",
        "ph": "ф",
        "wh": "в",
        "ck": "к",
        "ee": "и",
        "oo": "у",
        "ea": "и",
        "ё": "е",
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

    word = word.lower()
    for en, ru in mapping.items():
        word = word.replace(en, ru)

    # return remove_repeating(word)
    return word
