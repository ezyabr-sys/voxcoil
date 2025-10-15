import aiofiles
import os
from typing import Tuple
from core.exeptions import VoiceProcessingError

class VoiceService:
    @staticmethod
    async def download_voice_file(file_id: str, bot) -> str:
        """Скачивание голосового сообщения"""
        try:
            file = await bot.get_file(file_id)
            file_path = file.file_path
            
            
            os.makedirs("temp", exist_ok=True)
            
            
            temp_voice_path = f"temp/voice_{file_id}.ogg"
            await bot.download_file(file_path, temp_voice_path)
            
            return temp_voice_path
            
        except Exception as e:
            raise VoiceProcessingError(f"Ошибка загрузки голосового сообщения: {str(e)}")
    
    @staticmethod
    async def save_audio_response(audio_data, user_id: int) -> str:
        """Сохранение аудио ответа"""
        try:
            os.makedirs("temp", exist_ok=True)
            output_path = f"temp/response_{user_id}.mp3"
            
            if hasattr(audio_data, 'read'):
                
                async with aiofiles.open(output_path, 'wb') as f:
                    await f.write(audio_data.read())
            else:
                
                async with aiofiles.open(output_path, 'wb') as f:
                    await f.write(audio_data)
            
            return output_path
            
        except Exception as e:
            raise VoiceProcessingError(f"Ошибка сохранения аудио: {str(e)}")
    
    @staticmethod
    def cleanup_files(*file_paths):
        """Очистка временных файлов"""
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except:
                pass