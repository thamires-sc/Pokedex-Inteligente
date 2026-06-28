from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "mistralai/mistral-7b-instruct:free"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    # CORS
    ALLOWED_ORIGINS: list[str] = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

    # PokéAPI
    POKEAPI_BASE_URL: str = "https://pokeapi.co/api/v2"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()