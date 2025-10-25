from aiogram import Router, F
from aiogram.types import Message, Voice
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from services.openai_service import OpenAIService
from services.voice_service import VoiceService
from core.exeptions import OpenAIServiceError
import logging
import os

router = Router()
logger = logging.getLogger(__name__)

def get_openai_service():
    
    try:
        service = OpenAIService()
        
        if hasattr(service, 'client') and service.client is not None:
            logger.info(" OpenAI сервис успешно инициализирован")
            return service
        else:
            logger.error(" OpenAI сервис создан, но клиент не инициализирован")
            return None
    except Exception as e:
        logger.error(f" Ошибка создания OpenAI сервиса: {e}")
        return None

def get_voice_service():
    
    return VoiceService()

@router.message(Command("start"))
async def cmd_start(message: Message):
   
    await message.answer(
        " Голосовой ассистент готов к работе!\n\n"
        "Просто отправьте голосовое сообщение или текст, "
        "и я отвечу голосовым сообщением!"
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    
    await message.answer(
        " Помощь по боту:\n\n"
        "• Отправьте голосовое сообщение - я преобразую его в текст, "
        "получу ответ от AI и озвучу ответ\n"
        "• Отправьте текстовое сообщение - я отвечу текстом\n\n"
        "Бот использует OpenAI для обработки запросов."
    )

@router.message(Command("test"))
async def cmd_test(message: Message):
   
    try:
        service = get_openai_service()
        if service is None:
            await message.answer(" Сервис OpenAI не инициализирован")
            return
        
        
        models = await service.client.models.list()
        model_count = len(models.data)
        
        await message.answer(f" Сервис OpenAI работает! Доступно моделей: {model_count}")
        
    except Exception as e:
        await message.answer(f" Ошибка тестирования: {str(e)}")


@router.message(F.voice | F.audio | F.document)
<<<<<<< HEAD
async def handle_voice_message(message: Message, state: FSMContext):
    """Обработка голосовых сообщений"""
=======
async def handle_voice_message(message: Message):
    
>>>>>>> 4560863a39e9d12190037f91d894d04e36fecce2
    user_id = message.from_user.id
    
    openai_service = get_openai_service()
    voice_service = get_voice_service()
    
    if openai_service is None:
        await message.reply(" Сервис OpenAI временно недоступен. Проверьте настройки.")
        return
    
    voice_path = None
    audio_response_path = None
    
    try:
        processing_msg = await message.reply(" Обрабатываю голосовое сообщение...")
        
        if message.voice:
            file_id = message.voice.file_id
        elif message.audio:
            file_id = message.audio.file_id
        else:
            file_id = message.document.file_id
        
        voice_path = await voice_service.download_voice_file(file_id, message.bot)
        
        await processing_msg.edit_text(" Преобразую речь в текст...")
        user_text = await openai_service.transcribe_audio(voice_path)
        
        if not user_text.strip():
            await processing_msg.edit_text("Не удалось распознать речь в сообщении")
            return
        
        await processing_msg.edit_text(f" Ваш вопрос: {user_text}\n\n Формирую ответ...")
        
       
        assistant_response, thread_id, response_metadata = await openai_service.get_assistant_response(user_text)
        
        
        await state.update_data(thread_id=thread_id)
        
        
        if response_metadata.get('file_citations'):
            citations_info = f"\n\n Источники: использовано {len(response_metadata['file_citations'])} цитат из документа"
            assistant_response += citations_info
        
        
        if len(assistant_response) > 4096:
            assistant_response = assistant_response[:4096] + "..."
        
        await processing_msg.edit_text(f" Ваш вопрос: {user_text}\n\n Ответ: {assistant_response}\n\n Создаю аудио ответ...")
        
        
        os.makedirs("temp", exist_ok=True)
        audio_response_path = f"temp/response_{user_id}_{message.message_id}.mp3"
        
        try:
            
            await openai_service.text_to_speech(assistant_response, audio_response_path)
            
           
            if os.path.exists(audio_response_path) and os.path.getsize(audio_response_path) > 0:
                with open(audio_response_path, 'rb') as audio_file:
                    await message.reply_voice(
                        voice=audio_file,
                        caption=" Аудио ответ:"
                    )
                await processing_msg.delete()
            else:
                
                await processing_msg.edit_text(
                    f" Ваш вопрос: {user_text}\n\n"
                    f" Ответ: {assistant_response}\n\n"
                    f" Не удалось создать аудио версию ответа"
                )
                
        except Exception as tts_error:
            logger.error(f"Ошибка TTS: {tts_error}")
            
            await processing_msg.edit_text(
                f" Ваш вопрос: {user_text}\n\n"
                f" Ответ: {assistant_response}\n\n"
                f" Аудио ответ временно недоступен"
            )
        
    except OpenAIServiceError as e:
        await message.reply(f" Ошибка сервиса: {str(e)}")
        logger.error(f"OpenAI Service Error: {str(e)}")
    except Exception as e:
        await message.reply(" Произошла непредвиденная ошибка при обработке сообщения")
        logger.error(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        
        if voice_path or audio_response_path:
            voice_service.cleanup_files(voice_path, audio_response_path)

@router.message(F.text)
<<<<<<< HEAD
async def handle_text_message(message: Message, state: FSMContext):
    """Обработка текстовых сообщений"""
=======
async def handle_text_message(message: Message):
   
>>>>>>> 4560863a39e9d12190037f91d894d04e36fecce2
    openai_service = get_openai_service()
    
    if openai_service is None:
        await message.reply(" Сервис OpenAI временно недоступен. Проверьте настройки.")
        return
    
    try:
        processing_msg = await message.reply(" Обрабатываю текстовое сообщение...")
        
        
        assistant_response, thread_id, response_metadata = await openai_service.get_assistant_response(message.text)
        
        
        await state.update_data(thread_id=thread_id)
        
        
        if response_metadata.get('file_citations'):
            citations_info = f"\n\n Источники: использовано {len(response_metadata['file_citations'])} цитат из документа"
            assistant_response += citations_info
        
        await processing_msg.edit_text(f" Ответ: {assistant_response}")
        
    except OpenAIServiceError as e:
        await message.reply(f" Ошибка сервиса: {str(e)}")
    except Exception as e:
        await message.reply(" Произошла непредвиденная ошибка")
        logger.error(f"Unexpected error: {str(e)}")
