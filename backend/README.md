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

## Domain Layer — Core Entities

We create the leanest set of canonical domain models we need for ingestion & RAG.

- `Document`
- `Chunk`
- `Site`

## Domain Service Interfaces (Abstractions)

These services describe *what* the system does, not *how*.

- `VectorStore` interface
- `EmbeddingProvider` interface
- `Retriever` interface

## Infrastructure Layer

- `DummyRetriever`

## Dependency Injection Container

- `Container`

## First API Route



