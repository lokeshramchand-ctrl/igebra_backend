from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # If these are missing from the .env file, FastAPI will throw a clear error on startup
    MONGODB_URI: str
    MONGODB_DB_NAME: str = "velar"
    
    MILVUS_HOST: str = "10.10.10.130"
    MILVUS_PORT: str = "19530"

    # Tell Pydantic to read from the .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Instantiate it once to be imported across the app
settings = Settings()