# RAG — Codebase Indexing

Semantic search over local codebases using `nomic-embed-text` (Ollama) + qdrant.

## Setup

### 1) Start qdrant

```bash
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
```

### 2) Pull the embedding model

```bash
OLLAMA_HOST=http://100.114.87.119:11434 ollama pull nomic-embed-text
```

### 3) Install dependencies

```bash
pip install qdrant-client ollama
```

### 4) Index a codebase

```bash
python3 index_codebase.py /path/to/repo
```

### 5) Query

```bash
python3 query_codebase.py "how does authentication work"
```

## Scripts

Coming soon — background agent is generating these from the claw-code mirror.

- `index_codebase.py` — walks a repo, chunks files, embeds with nomic-embed-text, stores in qdrant
- `query_codebase.py` — embeds query, retrieves top-k chunks, prints with file paths

## Configuration

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server address |
| `QDRANT_URL` | `http://localhost:6333` | qdrant address |
| `COLLECTION` | `codebase` | qdrant collection name |
| `CHUNK_SIZE` | `500` | characters per chunk |
| `TOP_K` | `5` | results to return per query |
