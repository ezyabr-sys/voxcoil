class OpenAIServiceError(Exception):
    
    pass

class VoiceProcessingError(OpenAIServiceError):
    
    pass

class AssistantError(OpenAIServiceError):
    
    pass
