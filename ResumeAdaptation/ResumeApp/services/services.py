# services.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
import random
from rest_framework.exceptions import ValidationError
from ResumeApp.models import Resume, Vacancy, ResumeAdaptation
from .llm_service import LLMService  # Импортируем LLM сервис
from .scoring_service import ScoringService  # Импортируем Scoring сервис


def run_resume_adaptation(resume: Resume, vacancy: Vacancy, language: str = 'ru') -> ResumeAdaptation:
    """
    Адаптирует резюме под вакансию с помощью LLM
    """

    # 1. Извлекаем навыки из текстов (если они еще не извлечены)
    if not resume.parsed_skills:
        resume_skills = LLMService.extract_skills(resume.text)
        resume.parsed_skills = resume_skills
        resume.save(update_fields=['parsed_skills'])
    else:
        resume_skills = resume.parsed_skills

    if not vacancy.parsed_skills:
        vacancy_skills = LLMService.extract_skills(vacancy.description)
        vacancy.parsed_skills = vacancy_skills
        vacancy.save(update_fields=['parsed_skills'])
    else:
        vacancy_skills = vacancy.parsed_skills

    # 2. Считаем скор ДО адаптации
    score_before = ScoringService.calculate_score(resume_skills, vacancy_skills)
    missing_skills_before = ScoringService.get_missing_skills(resume_skills, vacancy_skills)

    # 3. Адаптируем резюме через LLM
    adapted_text = LLMService.adapt_resume(
        resume_text=resume.text,
        vacancy_text=vacancy.description,
        language=language  # 👈 Нужно добавить параметр языка в метод adapt_resume
    )

    # 4. Извлекаем навыки из адаптированного резюме
    adapted_skills = LLMService.extract_skills(adapted_text)

    # 5. Считаем скор ПОСЛЕ адаптации
    score_after = ScoringService.calculate_score(adapted_skills, vacancy_skills)

    # 6. Создаем запись об адаптации
    adaptation = ResumeAdaptation.objects.create(
        resume=resume,
        vacancy=vacancy,
        language=language,
        status='success',
        adapted_text=adapted_text,
        score_before=score_before,
        score_after=score_after,
        changes_log={
            "original_skills": resume_skills,
            "vacancy_skills": vacancy_skills,
            "missing_skills_before": missing_skills_before,
            "added_skills": list(set(adapted_skills) - set(resume_skills)),
            "score_improvement": score_after - score_before
        }
    )

    return adaptation


def get_resume_and_vacancy(resume_id: int, vacancy_id: int):
    """Получает резюме и вакансию из БД"""
    try:
        resume = Resume.objects.get(id=resume_id)
        vacancy = Vacancy.objects.get(id=vacancy_id)
    except (Resume.DoesNotExist, Vacancy.DoesNotExist):
        raise ValidationError("Резюме или вакансия с указанным ID не существует.")

    return resume, vacancy