import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from core.config import settings
from handlers.voice_handler import router as voice_router

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

async def main():
    
    if not settings.bot_token:
        logger.error(" BOT_TOKEN не найден!")
        return
    
    try:
        bot = Bot(token=settings.bot_token)
        dp = Dispatcher()
        
        
        dp.include_router(voice_router)
        
        logger.info(" Бот запускается...")
        
        
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f" Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
else:
    print("unluck")
