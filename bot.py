import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
from core.config import settings
from handlers.voice_handler import router as voice_router


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

class UserState(StatesGroup):
    active = State()

async def set_bot_commands(bot: Bot):
    """Установка команд меню для бота"""
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/reset", description="Сбросить историю"),
    ]
    await bot.set_my_commands(commands)

async def on_startup(bot: Bot):
    await set_bot_commands(bot)
    me = await bot.get_me()
    logger.info(f" Бот @{me.username} успешно запущен!")
    logger.info(" Используется MemoryStorage (Redis не доступен)")

async def main():
    try:
        if not settings.bot_token:
            logger.error(" BOT_TOKEN не найден!")
            return
        
        logger.info(" Инициализация бота...")
        
        
        storage = MemoryStorage()
        
        
        bot = Bot(
            token=settings.bot_token, 
            default=DefaultBotProperties(parse_mode="HTML")
        )
        
        dp = Dispatcher(storage=storage)
        
      
        dp.include_router(voice_router)
        dp.startup.register(on_startup)
        
        logger.info(" Бот запускается с MemoryStorage...")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f" Ошибка при запуске: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info(" Бот остановлен")
    except Exception as e:
        logger.error(f" Непредвиденная ошибка: {e}")