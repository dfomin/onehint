import pytest

from onehint.checkers import v3


@pytest.mark.parametrize("word, expected_result",
                         [
                             ("Берёза", "береза"),
                             ("Shweppes", "швепес"),
                         ])
def test_normalize(word: str, expected_result: str):
    assert v3.normalize(word) == expected_result


@pytest.mark.parametrize("word1, word2, expected_result",
                         [
                             ("Грех", "орех", False),
                             ("Собака", "собачий", True),
                             ("test", "test", True),
                             ("test", "asdf", False),
                         ])
def test_is_duplicates(word1: str, word2: str, expected_result: bool):
    assert v3.is_duplicates(word1, word2) == expected_result
