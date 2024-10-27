from openai import OpenAI

from onehint.checkers.base import BaseAPIVersion


PROMPT = """
You get two words from Russian language provided letter by letter. Define is they have the same root. If you don't know the word, consider it's a name. Reply only `true` or `false`.
"""


class APIv4(BaseAPIVersion):
    def __init__(self):
        self.client = OpenAI()

    def is_duplicates(self, word1: str, word2: str) -> bool:
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": [{"text": PROMPT, "type": "text"}]},
                {"role": "user", "content": [{"text": f"{" ".join(word1)}, {" ".join(word2)}", "type": "text"}]}
            ],
            temperature=0,
            top_p=1,
            max_tokens=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={
                "type": "text"
            }
        )
        result = completion.choices[0].message.content
        # print(completion)
        # print(word1, word2, result)
        if result.lower() == "true":
            return True
        elif result.lower() == "false":
            return False
        raise ValueError

    def normalize(self, word: str) -> str:
        return word
