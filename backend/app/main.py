from fastapi import FastAPI

app = FastAPI(
    title="AuroraRAG Backend",
    version="0.1.0",
    description="RAG-based search engine backend."
)

@app.get("/health")
def health():
    return {"status": "ok"}