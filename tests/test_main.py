import pytest

from justone_compare.main import WordPair, is_duplicates, find_duplicates, RoundWords


@pytest.mark.parametrize("word1, word2, expected_result",
                         [
                             ("Гребец", "Грести", False),
                             ("Грех", "орех", False),
                             ("Палец", "палка", False),
                             ("Палец", "пальма", False),
                             ("мошенники", "моё", False),
                             ("Один", "Одиссей", False),
                             ("Морозильник", "морг", False),
                             ("Д", "Дрейк", False),
                             ("Ну", "не", False),
                             ("Как", "Кайфу", False),
                             ("Морозильник", "Холодильник", False),
                             ("ка", "Караван", False),
                             ("Леонардо", "Лувр", False),
                             ("парламентский", "Парад", False),
                             ("сэр", "сыр", False),
                             ("Гребец", "Грех", False),
                             ("Плов", "Плошка", False),
                             ("рельеф", "-рельса", False),
                             ("лопатка", "копать", False),
                             ("Древнерусская", "древнерусская", True),
                             ("Антогонистка", "Антагонистка", True),
                             ("Снаряд", "наряд", True),
                             ("аллопеция", "Алопеция", True),
                             ("Джонатан", "Джонотан", True),
                             ("шоколада", "шоколадная", True),
                             ("Нитка", "Нитки", True),
                             ("рог", "рогатый", True),
                             ("Гну", "Гни", True),
                             ("Гни", "Гнить", True),
                             ("Ни", "Они", True),
                             ("Собака", "Собачий", True),
                             ("пустынный", "Пустыня", True),
                             ("дочка", "дочь", True),
                             ("Пластинки", "грампластинка", True),
                             ("согревающий", "Разогревающая", True),
                             ("Красножопая", "Жопа", True),
                             ("Дождевая", "Дождь", True),
                             ("bing", "бинг", True),
                             ("Лепить", "Лепка", True),
                             ("Лепнина", "Лепка", True),
                             ("алое", "алоэ", True),
                             ("Колечко", "Кольцо", True),
                             ("сова", "Сову", True),
                         ])
def test_is_duplicates(word1: str, word2: str, expected_result: bool):
    assert is_duplicates(WordPair(word1=word1, word2=word2)) == expected_result


@pytest.mark.parametrize("words, expected_result",
                         [
                             (["Дождевая", "Дождь"], [True, True]),
                         ])
def test_find_duplicates(words: list[str], expected_result: list[bool]):
    assert find_duplicates(RoundWords(words=words)).words == expected_result