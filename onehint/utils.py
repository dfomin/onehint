def fuzzy_common_size(word1: str, word2: str, fraction: int = 5) -> int:
    assert len(word1) <= len(word2)

    result = 0
    for i in range(len(word2) - len(word1) + 1 + (1 if len(word1) > 0 else 0)):
        skipped = 0
        current = 0
        for j in range(len(word1)):
            if i + j < len(word2) and word1[j] == word2[i + j]:
                current += 1
            elif skipped < len(word1) // fraction:
                skipped += 1
            else:
                break
        result = max(result, current)
    return result


def remove_repeating_letters(word: str) -> str:
    result = ""
    result += word[0]
    for ch in word[1:]:
        if ch.isalpha() and result[len(result) - 1] == ch:
            continue
        else:
            result += ch
    return result
