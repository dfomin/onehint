from typing import Callable

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from onehint.checkers import v1, v2

app = FastAPI()


class RoundWords(BaseModel):
    words: list[str]


class RoundDuplicates(BaseModel):
    words: list[list[int]]


class WordPair(BaseModel):
    word1: str
    word2: str


class VersionInfo(BaseModel):
    version: int
    description: str


@app.post("/version")
def version() -> int:
    return 2


@app.post("/versions_info")
def versions_info() -> list[VersionInfo]:
    return [
        VersionInfo(
            version=1,
            description="Original sivyhk's algorithms from C#"
        ),
        VersionInfo(
            version=2,
            description="Improved english letters mapping"
        )
    ]


@app.post("/v1/find_duplicates")
def find_duplicates_v1(round_words: RoundWords) -> RoundDuplicates:
    return find_duplicates(round_words, is_duplicates_v1)


@app.post("/v2/find_duplicates")
def find_duplicates_v2(round_words: RoundWords) -> RoundDuplicates:
    return find_duplicates(round_words, is_duplicates_v2)


def find_duplicates(round_words: RoundWords, is_duplicates: Callable[[WordPair], bool]) -> RoundDuplicates:
    duplicates = [[] for _ in range(len(round_words.words))]
    for i in range(len(duplicates)):
        for j in range(i + 1, len(duplicates)):
            if is_duplicates(WordPair(word1=round_words.words[i], word2=round_words.words[j])):
                duplicates[i].append(j)
                duplicates[j].append(i)
    return RoundDuplicates(words=duplicates)


@app.post("/v1/is_duplicates")
def is_duplicates_v1(pair: WordPair) -> bool:
    return v1.is_duplicates(pair.word1, pair.word2)


@app.post("/v2/is_duplicates")
def is_duplicates_v2(pair: WordPair) -> bool:
    return v2.is_duplicates(pair.word1, pair.word2)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
