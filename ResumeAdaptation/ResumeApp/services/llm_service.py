from openai import OpenAI
from django.conf import settings

# OpenRouter использует OpenAI-совместимый API
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.GROQ_API_KEY,  # Ваш ключ sk-or-v1-...
    default_headers={
        "HTTP-Referer": "http://localhost:8000",  # Для статистики OpenRouter
        "X-Title": "Resume Adaptation App",
    }
)


class LLMService:

    @staticmethod
    def test_connection():
        response = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct",  # Другой формат имени модели
            messages=[
                {
                    "role": "user",
                    "content": "Say hello"
                }
            ]
        )
        return response.choices[0].message.content

    @staticmethod
    def extract_skills(text: str):
        prompt = f"""
        Извлеки из текста только конкретные профессиональные навыки.

        Правила:
        - верни только навыки
        - без категорий
        - без описаний
        - без предложений
        - без нумерации
        - только список через запятую

        Пример правильного ответа:
        Python, Django, PostgreSQL, Docker

        Текст:
        {text}
        """

        response = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # Для извлечения навыков лучше низкая температура
            max_tokens=500
        )

        content = response.choices[0].message.content

        skills = [
            skill.strip()
            for skill in content.split(",")
            if skill.strip()
        ]

        return list(set(skills))

    @staticmethod
    def adapt_resume(resume_text: str, vacancy_text: str, language: str = 'ru'):
        """
        Адаптирует резюме под вакансию с учетом языка
        """

        language_prompt = {
            'ru': 'Ответ должен быть на РУССКОМ языке.',
            'en': 'Response must be in ENGLISH language.'
        }

        prompt = f"""
        Ты HR-специалист и ATS-оптимизатор.

        {language_prompt.get(language, 'Ответ на русском языке')}

        Твоя задача:
        - адаптировать резюме под вакансию
        - сделать текст более релевантным
        - добавить релевантные навыки из вакансии
        - улучшить ATS-совместимость
        - сохранить правдивость информации (не выдумывай несуществующий опыт)

        Вакансия:
        {vacancy_text}

        Резюме:
        {resume_text}

        Верни ТОЛЬКО адаптированное резюме, без комментариев и пояснений.
        """

        response = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )

        return response.choices[0].message.content