import os
from sentence_transformers import SentenceTransformer, util

from fastapi import FastAPI
from pydantic import BaseModel

model = "all-mpnet-base-v2"
# nq-distilbert-base-v1

rb_pages_dir = "data/text"

embedder = SentenceTransformer(model)

# Corpus of rules lines
lines = []
for file in os.listdir(rb_pages_dir):
    filename = os.fsdecode(file)
    with open(os.path.join(rb_pages_dir, filename)) as f:
        # Try encoding passages as [title, text] instead too
        game,page = filename.split('.')[0].split('_')
        lines += map(str.strip, f.readlines())
        print(f"Loaded {game} page {page}")

print("Embedding rulebook lines:")
# # Use "convert_to_tensor=True" to keep the tensors on GPU (if available)
corpus_embeddings = embedder.encode(lines, convert_to_tensor=True)

print("Done!")

# Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
top_k = 5

app = FastAPI()

class Query(BaseModel):
    game: str
    question: str

class Response(BaseModel):
    documents: list[str] = []

@app.post("/query")
async def query(query: Query) -> Response:
    query_embedding = embedder.encode(query.question, convert_to_tensor=True)

    # Alternatively, we can also use util.semantic_search to perform cosine similarty + topk
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=5)
    hits = hits[0]      #Get the hits for the first query
    docs = list(map(lambda hit : lines[hit["corpus_id"]], hits))
    return Response(documents=docs)
