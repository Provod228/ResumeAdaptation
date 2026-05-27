from rest_framework import serializers

from ResumeApp.models import Resume, Vacancy, ResumeAdaptation


class AdaptationRequestSerializer(serializers.Serializer):
    """Сериализатор для валидации входящих данных POST-запроса"""
    resume_id = serializers.IntegerField(help_text="ID исходного резюме")
    vacancy_id = serializers.IntegerField(help_text="ID вакансии, под которую адаптируется резюме")
    language = serializers.ChoiceField(
        choices=['ru', 'en'],
        default='ru',
        help_text="Язык вывода (ru или en)"
    )

    def validate_resume_id(self, value):
        if not Resume.objects.filter(id=value).exists():
            raise serializers.ValidationError("Резюме с указанным ID не существует.")
        return value

    def validate_vacancy_id(self, value):
        if not Vacancy.objects.filter(id=value).exists():
            raise serializers.ValidationError("Вакансия с указанным ID не существует.")
        return value





class ResumeAdaptationResponseSerializer(serializers.ModelSerializer):
    """Сериализатор для формирования ответа с результатами адаптации"""
    resume_title = serializers.CharField(source='resume.title', read_only=True)
    vacancy_title = serializers.CharField(source='vacancy.title', read_only=True)

    class Meta:
        model = ResumeAdaptation
        fields = [
            'id',
            'status',
            'resume_title',
            'vacancy_title',
            'score_before',
            'score_after',
            'adapted_text',
            'changes_log',
            'created_at'
        ]


class ResumeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Resume"""

    class Meta:
        model = Resume
        fields = [
            'id',
            'title',
            'text',
            'parsed_skills',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ========== Сериализаторы для Vacancy ==========

class VacancySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Vacancy"""

    class Meta:
        model = Vacancy
        fields = [
            'id',
            'title',
            'company',
            'description',
            'url',
            'parsed_skills',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']