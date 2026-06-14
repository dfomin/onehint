# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A FastAPI service for the word game "Just One" (Однажды / OneHint). It exposes endpoints that decide whether two clue words are "duplicates" (effectively the same word / same root) so the game can reject colliding clues, plus a per-game player statistics report pulled from a PostgreSQL database.

## Commands

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. Python 3.12 (pinned in `.python-version`).

```bash
uv sync                                 # create/refresh .venv from uv.lock (includes dev deps)

# Run the server locally (reads onehint/main.py __main__ block)
uv run python -m onehint.main           # serves on 0.0.0.0:8000
uv run uvicorn onehint.main:app --reload  # dev with autoreload

# Tests
uv run pytest                           # full suite
uv run pytest tests/checkers/test_v1.py # one file
uv run pytest tests/checkers/test_v1.py::test_is_duplicates  # one test

# Dependencies
uv add <pkg>                            # runtime dep        (updates pyproject.toml + uv.lock)
uv add --dev <pkg>                      # dev-only dep
# After any dependency change, regenerate the pip lockfile the Docker build consumes:
uv export --no-dev --frozen --no-hashes -o requirements.txt

# Docker (mirrors CI/production)
docker build -t onehint .
docker run -p 8000:8000 onehint
```

`pyproject.toml` is the source of truth for dependencies (direct deps under `[project.dependencies]`, pytest under `[dependency-groups].dev`); `uv.lock` is the resolved, committed lockfile. `uv` is configured with `package = false`, so the `onehint` package is run from the working directory, not installed. **`requirements.txt` is a generated artifact** (`uv export` of the non-dev lock) kept only so the pip-based Dockerfile stays unchanged — never edit it by hand; regenerate it after changing dependencies.

The `/statistics` endpoint requires a live Postgres connection via env vars `DATABASE`, `HOST`, `PORT`, `USER`, `PASSWORD` (read in `onehint/statistics/players_statistics.py`). Everything else (duplicate checking) runs with no external services.

## Architecture

**Versioned checker algorithms.** The core is a family of duplicate-detection algorithms, one per version, in `onehint/checkers/v1.py` … `v5.py`. Each is a class `APIv{N}` subclassing `BaseAPIVersion` (`checkers/base.py`) and implementing two methods:
- `normalize(word)` — lowercases and transliterates Latin → Cyrillic (each version refines the mapping; v5 also strips Unicode diacritics and handles digraphs like `sh`→`ш`).
- `is_duplicates(word1, word2)` — the heuristic comparison (Levenshtein distance + longest-common-substring / fuzzy-common-substring thresholds). This is the only method versions must define; the base class derives `find_duplicates` (pairwise over a round) and `players_statistics` from it.

Versions are **append-only and immutable**: each new version is a copy-and-tweak of the previous algorithm, never an in-place edit, because old versions stay routed for backward compatibility. v4 ("Asking ChatGPT", an OpenAI-backed checker) exists but is commented out everywhere.

**Routing is generated, not hand-written.** `onehint/main.py` builds an identical `APIRouter` for each version via `create_version_router(api_class)`, mounting them under `/v1`, `/v2`, … `/v5`. The current latest version number is returned by the `/version` endpoint (currently `5`); `create_latest_router()` reflects on that number to also mount the latest algorithm at the **root** (unprefixed) path. So `POST /find_duplicates` == `POST /v5/find_duplicates`. When adding a version: create `onehint/checkers/vN.py`, bump the `version()` return value, add a `VersionInfo` entry in `versions_info()`, and add the `include_router(... prefix="/vN")` line.

Each router exposes: `POST /find_duplicates` (a whole round of words → list of duplicate-index lists), `POST /is_duplicates` (a single pair → bool), `GET /statistics` (game_id → plain-text report).

**Shared math** lives in `onehint/utils.py`: `fuzzy_common_size` (longest common substring allowing a fraction of mismatches), `remove_repeating_letters`, and `wilson_score` (used for ranking players).

**Statistics** (`onehint/statistics/players_statistics.py`) queries Postgres with a single hard-coded join over `Rounds`/`PlayerRounds`/`Players`, loads it into a Polars DataFrame, and aggregates per-player guess accuracy, "clown" (bad-clue) rates, and clown pairs. Note the magic numbers from the game schema: `Role` 1 = guesser / 2 = cluer; `Result` 1 = good clue / 2 = clown; `Status` 8 = completed. It calls back into a version's `is_duplicates` to detect colliding clown clues.

## Conventions & gotchas

- The domain is Russian-language: clue words, the `normalize` mappings, and the `is_duplicates` test cases are all Cyrillic. Latin input is transliterated to Cyrillic before comparison.
- Tests under `tests/checkers/` are per-version and consist of large `parametrize` tables of real word pairs with expected booleans — the source of truth for tuning thresholds. When changing an algorithm, expect to extend these tables rather than rewrite assertions.
- `onehint/statistics/info.py` is an offline analysis script (run directly) that scores every version against `datasets/data.json` to compare accuracy; it is not part of the served app.
- `chatgpt.txt` and `test.sh` are scratch/experiment files (test.sh is a raw OpenAI curl for the v4 idea), not part of the build.
- CI (`.github/workflows/docker-publish.yml`) builds and pushes a Docker image to Docker Hub on every push to `main`; it does **not** run pytest.
