class OpenAIServiceError(Exception):
    """Базовое исключение для сервиса OpenAI"""
    pass

class VoiceProcessingError(OpenAIServiceError):
    """Ошибка обработки голосовых сообщений"""
    pass

class AssistantError(OpenAIServiceError):
    """Ошибка работы с Assistant API"""
    pass