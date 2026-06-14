from openai import OpenAI

from onehint.checkers.base import BaseAPIVersion


# PROMPT = """
# You get two words from Russian language provided letter by letter. Define is they have the same root. If you don't know the word, consider it's a name. Reply only `true` or `false`.
# """
PROMPT = """
Даны два слова на русском языке. Нужно определить являются ли они однокоренными. Если слово незнакомо, считай что это имя собственное. Отвечай только `true` если однокоренные, иначе `false`.
"""


class APIv4(BaseAPIVersion):
    def __init__(self):
        self.client = OpenAI()

    def is_duplicates(self, word1: str, word2: str) -> bool:
        response = self.client.responses.create(
            model="gpt-4.1-mini-2025-04-14",
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": PROMPT
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": f"{" ".join(word1)}, {" ".join(word2)}"
                        }
                    ]
                }
            ],
            text={
                "format": {
                    "type": "text"
                }
            },
            reasoning={},
            tools=[],
            temperature=0,
            max_output_tokens=16,
            top_p=1,
            store=False
        )
        result = response.output[0].content[0].text
        print(result)
        print(word1, word2, result)
        if result.lower() == "true":
            return True
        elif result.lower() == "false":
            return False
        raise ValueError

    def normalize(self, word: str) -> str:
        return word
