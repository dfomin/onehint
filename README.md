```bash
docker build -t onehint .
docker run -p 8000:8000 onehint
curl -X POST "http://127.0.0.1:8000/find_duplicates" -H "Content-Type: application/json" -d '{"words": ["hello", "hell", "asdf"]}'

# Expected response: {"words":[[1],[0],[]]}

curl -X GET "http://127.0.0.1:8000/statistics" -H "Content-Type: application/json" -d '{"game_id": 123}'

# Expected response (plain string with newlines):
# Guesses:
# player1 0.5 50%
# ...
# etc
```