from abc import ABC

from onehint.statistics.players_statistics import PlayerStatistics


class BaseAPIVersion(ABC):
    def find_duplicates(self, round_words: list[str]) -> list[list[int]]:
        duplicates = [[] for _ in range(len(round_words))]
        for i in range(len(duplicates)):
            for j in range(i + 1, len(duplicates)):
                if self.is_duplicates(round_words[i], round_words[j]):
                    duplicates[i].append(j)
                    duplicates[j].append(i)
        return duplicates

    def players_statistics(self, game_id: int) -> str:
        return PlayerStatistics().statistics(game_id, self.is_duplicates)

    def is_duplicates(self, word1: str, word2: str) -> bool:
        raise NotImplementedError

    def normalize(self, word: str) -> str:
        raise NotImplementedError
