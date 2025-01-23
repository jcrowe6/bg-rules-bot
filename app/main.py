from fastapi import FastAPI, Depends
from pydantic import BaseModel
from functools import lru_cache
from typing_extensions import Annotated

import requests

from . import config

class Query(BaseModel):
    game: str
    question: str

class RetrievalResponse(BaseModel):
    documents: list[str]

class Response(BaseModel):
    answer: str

app = FastAPI()
s = config.Settings()

# @lru_cache
def get_settings():
    return config.Settings()

@app.post("/query")
async def query(query: Query, settings: Annotated[config.Settings, Depends(get_settings)]) -> Response:
    # 1 Call retrieval service with game and question
    print(settings)
    url = "http://localhost:8001"
    retr_response = RetrievalResponse.model_validate(requests.post(f"{url}/query", json={"game": query.game, "question": query.question}).json())

    # 2 Call LLM service with relevant snippets
    
    # Return generated response
    return Response(answer=f'{retr_response.documents[0]}')