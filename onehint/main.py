from typing import Callable

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

from onehint.checkers.v1 import APIv1
from onehint.checkers.v2 import APIv2

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


def create_version_router(api_class: Callable) -> APIRouter:
    router = APIRouter()
    api = api_class()

    @router.post("/find_duplicates")
    def find_duplicates(round_words: RoundWords) -> RoundDuplicates:
        return RoundDuplicates(words=api.find_duplicates(round_words.words))

    @router.post("/is_duplicates")
    def is_duplicates(pair: WordPair) -> bool:
        return api.is_duplicates(pair.word1, pair.word2)

    return router


app.include_router(create_version_router(APIv1), prefix="/v1")
app.include_router(create_version_router(APIv2), prefix="/v2")


@app.get("/version")
def version() -> int:
    return 2


@app.get("/versions_info")
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
