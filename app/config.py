from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "BGRB RAG Service"
    env: str = "local"
    retrieval_service_url: str 
    generation_service_url: str
    model_config  = SettingsConfigDict(env_file=".env")