import pytest

from onehint.utils import fuzzy_common_size, remove_repeating_letters


@pytest.mark.parametrize("word1, word2, expected_result",
                         [
                             ("abcdefgh", "abcdzfgh", 7),
                             ("defaaa", "abcdefgh", 3),
                         ])
def test_fuzzy_common_size(word1: str, word2: str, expected_result: int):
    assert fuzzy_common_size(word1, word2) == expected_result


@pytest.mark.parametrize("word, expected_result",
                         [
                             ("abcdef", "abcdef"),
                             ("aabbcccdeff", "abcdef"),
                             ("007", "007"),
                             ("aa0aa", "a0a"),
                             ("aa00aa", "a00a"),
                         ])
def test_remove_repeating_letters(word: str, expected_result: str):
    assert remove_repeating_letters(word) == expected_result
