```bash
docker build -t onehint .
docker run -p 8000:8000 onehint
curl -X POST "http://127.0.0.1:8000/v1/find_duplicates" -H "Content-Type: application/json" -d '{"words": ["hello", "hell", "asdf"]}'

# Expected response: {"words":[[1],[0],[]]}
```