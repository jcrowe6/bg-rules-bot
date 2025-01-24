from fastapi import FastAPI, Depends
from pydantic import BaseModel
from functools import lru_cache
from typing_extensions import Annotated

import requests

from .config import Settings

class RAGQuery(BaseModel):
    game: str
    question: str

class RAGResponse(BaseModel):
    answer: str

class RetrievalQuery(BaseModel):
    game: str
    question: str

class RetrievalResponse(BaseModel):
    documents: list[str]

class GenerationQuery(BaseModel):
    model: str = "llama3.1"
    stream: bool = False
    prompt: str

class GenerationResponse(BaseModel):
    response: str

app = FastAPI()

# @lru_cache
def get_settings():
    return Settings()

def get_prompt(question: str, documents: list[str]) -> str:
    return  f"Rulebook lines:\n{'\n'.join(documents)}\n \
            User question: \"{question}\"\n \
            Instruction:\n \
            Provide a short answer to the user's rules question, referencing the rulebook lines above. Don't preface it."

@app.post("/query") 
async def query(query: RAGQuery, settings: Annotated[Settings, Depends(get_settings)]) -> RAGResponse:
    # 1 Call retrieval service with game and question
    retr_query = RetrievalQuery(game=query.game, question=query.question)
    retr_response_json = requests.post(f"{settings.retrieval_service_url}/query", json=retr_query.model_dump()).json()
    retr_response = RetrievalResponse.model_validate(retr_response_json)
    # 2 Call LLM service with relevant snippets
    prompt = get_prompt(query.question, retr_response.documents)
    print(prompt)
    gen_query = GenerationQuery(prompt=prompt)
    gen_response = requests.post(f"{settings.generation_service_url}/api/generate", json=gen_query.model_dump())
    gen_response = GenerationResponse.model_validate(gen_response.json())

    # Return generated response
    return RAGResponse(answer=gen_response.response)