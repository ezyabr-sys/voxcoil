from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os

class Settings(BaseSettings):
    
    bot_token: str = Field(..., env="BOT_TOKEN")
    
    
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    assistant_id: str = Field(..., env="ASSISTANT_ID")
    
    
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    
    
    document_path: str = Field("documents/тревожность.docx", env="DOCUMENT_PATH")
    vector_store_id: Optional[str] = Field(None, env="VECTOR_STORE_ID")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()