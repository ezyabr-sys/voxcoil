import logging
from openai import AsyncOpenAI
from core.config import settings
from core.exeptions import OpenAIServiceError
import os

logger = logging.getLogger(__name__)

class DocumentService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def create_vector_store(self, file_path: str) -> str:
        """Создание vector store и загрузка документа"""
        try:
            
            vector_store = await self.client.beta.vector_stores.create(
                name="Тревожность Документы"
            )
            
           
            with open(file_path, "rb") as file:
                file_stream = await self.client.beta.vector_stores.file_batches.upload_and_poll(
                    vector_store_id=vector_store.id,
                    files=[file]
                )
            
            logger.info(f" Vector store создан: {vector_store.id}")
            logger.info(f" Файлы загружены: {file_stream.file_counts}")
            
            return vector_store.id
            
        except Exception as e:
            logger.error(f" Ошибка создания vector store: {e}")
            raise OpenAIServiceError(f"Ошибка загрузки документа: {str(e)}")
    
    async def update_assistant_with_files(self, assistant_id: str, vector_store_id: str):
        """Обновление ассистента с file_search"""
        try:
            assistant = await self.client.beta.assistants.update(
                assistant_id=assistant_id,
                tools=[{"type": "file_search"}],
                tool_resources={
                    "file_search": {
                        "vector_store_ids": [vector_store_id]
                    }
                }
            )
            logger.info(f" Ассистент обновлен с file_search: {assistant.id}")
            return assistant
            
        except Exception as e:
            logger.error(f" Ошибка обновления ассистента: {e}")
            raise OpenAIServiceError(f"Ошибка обновления ассистента: {str(e)}")