import openai
from openai import AsyncOpenAI
from core.config import settings
from core.exeptions import AssistantError, VoiceProcessingError
import logging
import os
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self._client = None
        self._assistant_id = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Инициализация клиента OpenAI с проверками"""
        try:
            logger.info(" Инициализация OpenAI клиента...")
            
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY не найден в настройках")
            
            self._client = AsyncOpenAI(api_key=settings.openai_api_key)
            self._assistant_id = settings.assistant_id
            
            logger.info(" OpenAI клиент успешно инициализирован")
            
        except Exception as e:
            logger.error(f" Ошибка инициализации OpenAI клиента: {e}")
            raise
    
    @property
    def client(self):
        if self._client is None:
            self._initialize_client()
        return self._client
    
    @property
    def assistant_id(self):
        if self._assistant_id is None:
            self._assistant_id = settings.assistant_id
        return self._assistant_id
    
    async def transcribe_audio(self, audio_file_path: str) -> str:
        """Транскрибация голосового сообщения в текст"""
        try:
            logger.info(f" Начинаем транскрибацию файла: {audio_file_path}")
            
            if not os.path.exists(audio_file_path):
                raise VoiceProcessingError(f"Аудио файл не найден: {audio_file_path}")
            
            with open(audio_file_path, "rb") as audio_file:
                transcription = await self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            
            logger.info(f" Транскрибация завершена: {transcription[:50]}...")
            return transcription
            
        except Exception as e:
            logger.error(f" Ошибка транскрибации: {e}")
            raise VoiceProcessingError(f"Ошибка транскрибации: {str(e)}")
    
    async def get_assistant_response(self, message: str, thread_id: Optional[str] = None) -> tuple[str, str, Dict[str, Any]]:
        """Получение ответа от Assistant API с информацией об источниках"""
        try:
            logger.info(f" Запрос к ассистенту: {message[:50]}...")
            
           
            if not thread_id:
                thread = await self.client.beta.threads.create()
                thread_id = thread.id
                logger.info(f" Создан новый тред: {thread_id}")
            
            
            await self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message
            )
            
            
            run = await self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=self.assistant_id
            )
            logger.info(f" Запущен процесс ассистента: {run.id}, статус: {run.status}")
            
            
            while run.status in ["queued", "in_progress"]:
                import asyncio
                await asyncio.sleep(1)
                run = await self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )
                logger.info(f" Статус процесса: {run.status}")
            if run.status == "completed":
               
                messages = await self.client.beta.threads.messages.list(
                    thread_id=thread_id
                )
                
                
                assistant_messages = [
                    msg for msg in messages.data 
                    if msg.role == "assistant"
                ]
                
                if assistant_messages:
                    latest_message = assistant_messages[0]
                    response_text = latest_message.content[0].text.value
                    
                   
                    file_citations = []
                    if hasattr(latest_message.content[0].text, 'annotations'):
                        for annotation in latest_message.content[0].text.annotations:
                            if hasattr(annotation, 'file_citation'):
                                file_citations.append({
                                    'file_id': annotation.file_citation.file_id,
                                    'quote': annotation.file_citation.quote
                                })
                    
                    logger.info(f" Получен ответ от ассистента: {response_text[:50]}...")
                    logger.info(f" Использовано цитат из файлов: {len(file_citations)}")
                    
                    return response_text, thread_id, {'file_citations': file_citations}
                else:
                    raise AssistantError("Ассистент не вернул сообщение")
            else:
                raise AssistantError(f"Процесс ассистента завершился со статусом: {run.status}")
            
        except Exception as e:
            logger.error(f" Ошибка Assistant API: {e}")
            raise AssistantError(f"Ошибка Assistant API: {str(e)}")
    
    async def text_to_speech(self, text: str, output_path: str) -> None:
        """Преобразование текста в речь"""
        try:
            logger.info(f" Создание аудио из текста: {text[:50]}...")
            
            response = await self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text
            )
            
            
            content = response.content
            with open(output_path, 'wb') as f:
                f.write(content)
                
            logger.info(f" Аудио файл создан: {output_path}")
            
        except Exception as e:
            logger.error(f" Ошибка TTS: {e}")
            raise VoiceProcessingError(f"Ошибка TTS: {str(e)}")