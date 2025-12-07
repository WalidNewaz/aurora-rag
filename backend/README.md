# Aurora RAG


## Install Dependencies

```commandline
poetry install
```

## Launch app

```commandline
poetry run uvicorn app.main:app --reload
```

## Run tests

```commandline
poetry run pytest
```

## Clean Architecture for This Project

Clean architecture separates:

* **domain**: core entities, business rules
* **application**: use cases, orchestrators
* **infrastructure**: DB, crawlers, providers
* **interfaces**: FastAPI routes, DTOs

Directory overview:

```
app/
  domain/
    models/       # Document, Chunk, Embedding, Job
    services/     # Abstract services (Retriever, VectorStore)
  application/
    use_cases/    # CrawlSite, EmbedChunks, RagQuery
  infrastructure/
    db/           # Postgres adapters
    crawling/     # Crawler impls
    llm/          # Ollama/OpenAI adapters
    vector/       # PGVector/Pinecone adapters
  api/
    routes/       # REST routes
    schemas/      # Pydantic schemas
  core/
    config.py
    logging.py
```