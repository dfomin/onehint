import os
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable

import psycopg2
import polars as pl

from onehint.utils import wilson_score

QUERY = '''
SELECT "RoundId", "DictionaryWordId", "IsWin", "Word", "Role", "PlayerRounds"."Status", "Result", "Name"
FROM "Rounds"
LEFT JOIN "PlayerRounds"
    ON "Rounds"."Id" = "PlayerRounds"."RoundId"
LEFT JOIN "Players"
    ON "PlayerRounds"."PlayerId" = "Players"."Id"
WHERE "Rounds"."GameId" = (%s)
'''


class DatabaseManager:
    def __init__(self):
        database = os.environ["DATABASE"]
        host = os.environ["HOST"]
        port = os.environ["PORT"]
        user = os.environ["USER"]
        password = os.environ["PASSWORD"]
        print(database)
        print(host)
        self.conn = psycopg2.connect(database=database, host=host, port=port, user=user, password=password)

    def fetchall(self, game_id: str) -> pl.DataFrame:
        cursor = self.conn.cursor()
        cursor.execute(QUERY, (game_id,))
        result = cursor.fetchall()
        df = pl.DataFrame(result, schema=[
            "RoundId",
            "DictionaryWordId",
            "IsWin",
            "Word",
            "Role",
            "Status",
            "Result",
            "Name"
        ])
        return df


@dataclass
class PlayerInfo:
    correct_guesses: int = 0
    guesses_count: int = 0
    hint_count: int = 0
    clown_count: int = 0
    good_hint_count: int = 0
    clowns: dict[str, int] = field(default_factory=lambda: defaultdict(int))

    def guess_score(self) -> float:
        return wilson_score(self.correct_guesses, self.guesses_count)

    def guess_ratio(self) -> float:
        return self.correct_guesses / self.guesses_count

    def good_hint_ratio(self) -> float:
        if self.hint_count - self.clown_count > 0:
            return self.good_hint_count / (self.hint_count - self.clown_count)
        else:
            return 0

    def clown_score(self, reverse: bool = False) -> float:
        if not reverse:
            return wilson_score(self.clown_count, self.hint_count)
        else:
            return 1 - wilson_score(self.hint_count - self.clown_count, self.hint_count)

    def clown_ratio(self):
        return self.clown_count / self.hint_count


class PlayerStatistics:
    def __init__(self):
        self.database = DatabaseManager()

    def statistics(self, game_id: str, is_duplicates: Callable[[str, str], bool]) -> str:
        df = self.database.fetchall(game_id)
        players = defaultdict(PlayerInfo)
        for round_id in df["RoundId"].unique():
            round_data = df.filter(pl.col("RoundId") == round_id)
            if len(round_data.filter((pl.col("Status") != 8) & (pl.col("Role") == 1))) > 0:
                continue
            guesser = round_data.filter(pl.col("Role") == 1).select("Name").to_series()[0]
            is_win = round_data.filter(pl.col("Role") == 1).select("IsWin").to_series()[0]
            if is_win:
                players[guesser].correct_guesses += 1
            players[guesser].guesses_count += 1

            cluers = round_data.filter((pl.col("Role") == 2) & (pl.col("Result") != 0)).select("Name").to_series().to_list()
            for cluer in cluers:
                players[cluer].hint_count += 1

            if is_win:
                non_clowns = round_data.filter((pl.col("Role") == 2) & (pl.col("Result") == 1)).select("Name").to_series().to_list()
                for cluer in non_clowns:
                    players[cluer].good_hint_count += 1

            clowns = round_data.filter((pl.col("Role") == 2) & (pl.col("Result") == 2)).select("Name").to_series().to_list()
            for cluer in clowns:
                players[cluer].clown_count += 1

            clown_clues = round_data.filter((pl.col("Role") == 2) & (pl.col("Result") == 2)).select("Word").to_series().to_list()
            assert len(clowns) == len(clown_clues)

            for i in range(len(clowns)):
                for j in range(i + 1, len(clowns)):
                    if is_duplicates(clown_clues[i], clown_clues[j]):
                        players[clowns[i]].clowns[clowns[j]] += 1
                        players[clowns[j]].clowns[clowns[i]] += 1

        response = "Guesses:\n"
        values = [(name, player.guess_score(), player.guess_ratio()) for name, player in players.items()]
        for result in sorted(values, key=lambda x: -x[1]):
            response += f"{result[0]} {result[1]:.2f} {round(100 * result[2])}%\n"

        response += "\nClowns:\n"
        values = [(name, player.clown_ratio()) for name, player in players.items()]
        for result in sorted(values, key=lambda x: x[1]):
            response += f"{result[0]} {round(100 * result[1])}%\n"

        response += "\nClown pairs:\n"
        for name, player in players.items():
            stats = sorted(player.clowns.items(), key=lambda x: -x[1])
            m = stats[0]
            stats = [(name, value) for name, value in stats if value == m[1]]
            response += f"{name} -> {stats[0][0]}\n"
        return response
