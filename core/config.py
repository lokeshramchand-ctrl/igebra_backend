from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGODB_URI: str
    MONGODB_DB_NAME: str = "velar"
    MILVUS_URI: str = "http://localhost:19530"
    OLLAMA_URI: str = "http://localhost:11434"   # <-- add this
    velar_api_key: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
