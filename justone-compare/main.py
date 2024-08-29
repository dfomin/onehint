from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class StringPair(BaseModel):
    string1: str
    string2: str


@app.post("/compare")
def compare_strings(pair: StringPair) -> bool:
    return pair.string1 == pair.string2
