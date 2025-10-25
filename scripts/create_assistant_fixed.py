import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def create_assistant_guaranteed():
    """Гарантированно рабочий способ создания ассистента"""
    
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        print(" OPENAI_API_KEY не найден в .env файле")
        return
    
    client = OpenAI(api_key=openai_api_key)
    
    try:
       
        print(" Создаем базового ассистента...")
        assistant = client.beta.assistants.create(
            name="Тревожность Ассистент",
            instructions="""Ты - эксперт по тревожности и психическому здоровью. 
Отвечай на вопросы о тревожности, ее симптомах, причинах и методах преодоления.
Основные темы, которые ты знаешь:
- Симптомы тревожности: учащенное сердцебиение, потливость, напряжение
- Причины: генетика, стресс, травмы
- Методы лечения: терапия, медитация, физическая активность
- Самопомощь: дыхательные упражнения, ведение дневника""",
            tools=[],  
            model="gpt-4-1106-preview"
        )
        
        print(f" Ассистент создан: {assistant.id}")
        
        
        env_file_path = project_root / '.env'
        with open(env_file_path, 'a') as f:
            f.write(f'\nASSISTANT_ID={assistant.id}\n')
    
        print(f"\n Добавлено в .env файл:")
        print(f"ASSISTANT_ID={assistant.id}")
        print("\n Вы можете позже добавить файлы через OpenAI Dashboard")
        
        return assistant.id
        
    except Exception as e:
        print(f" Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_assistant_guaranteed()