```bash
docker build -t justone-compare .
docker run -p 8000:8000 justone-compare
curl -X POST "http://127.0.0.1:8000/find_duplicates" -H "Content-Type: application/json" -d '{"words": ["hello", "hell", "asdf"]}'

# Expected response: {"words":[true,true,false]}
```