import random

from rest_framework.exceptions import ValidationError

from ResumeApp.models import Resume, Vacancy, ResumeAdaptation


def run_resume_adaptation(resume: Resume, vacancy: Vacancy, language: str = 'ru') -> ResumeAdaptation:
    # Теперь при создании адаптации фиксируем язык
    adaptation = ResumeAdaptation.objects.create(
        resume=resume,
        vacancy=vacancy,
        language=language,
        status='success',
        adapted_text=f"[{language.upper()}] Адаптированный текст на основе вакансии {vacancy.title}:\n{resume.text}",
        score_before=random.randint(40, 60),
        score_after=random.randint(80, 98),
        changes_log={"added_skills": ["Python", "Django", "REST API"]}
    )
    return adaptation



def get_resume_and_vacancy(resume_id: int, vacancy_id: int):
    try:
        resume = Resume.objects.only('title', 'text', 'parsed_skills').get(id=resume_id)
        vacancy = Vacancy.objects.only('title', 'company', 'description', 'url', 'parsed_skills').get(id=vacancy_id)
    except (Resume.DoesNotExist, Vacancy.DoesNotExist):  # Используем кортеж
        raise ValidationError("Резюме или вакансия с указанным ID не существует.")

    return resume, vacancy