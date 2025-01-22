from fastapi import FastAPI
from pydantic import BaseModel

class Query(BaseModel):
    game: str
    question: str

class Response(BaseModel):
    answer: str

app = FastAPI()


@app.post("/query")
async def query(query: Query) -> Response:
    # 1 Call retrieval service with game and question

    # 2 Call LLM service with relevant snippets

    # Return generated response
    return Response(answer=f'Cool answer to your {query.game} question: {query.question}')