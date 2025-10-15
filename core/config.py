from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    bot_token: str = Field(..., env="BOT_TOKEN")
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    assistant_id: str = Field(..., env="ASSISTANT_ID")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()