# Aurora RAG

Aurora RAG is a general purpose Retrieval Augmented Generation pipeline.
It provides the following features:

1. Source registration
2. Artifact Ingestion
3. Retrieval

## Ingestion Pipeline

The Ingestion Pipeline is a major component of the system.
It consists of the following subsystems:

1. **Crawler**: produces artifacts
2. **Parser**: produces canonical documents from artifacts
3. **Chunker**: produces chunks from documents
4. **Embedder**: produces vector embeddings of chunks


## Artifact Lifecycle (Phase 1 – Upload)

1. User uploads file via `/sources/{id}/upload`
2. `ArtifactService.store_upload`:
   - writes file to disk
   - inserts `artifacts` row
3. API returns `artifact_id`
4. No parsing occurs yet

Later phases:

- Artifact parsing
- Document creation
- Chunking
- Embedding

Each phase is triggered asynchronously.