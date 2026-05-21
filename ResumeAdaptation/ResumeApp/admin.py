from django.contrib import admin
from .models import Resume, Vacancy, ResumeAdaptation


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    list_display_links = ('title',)
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'text')
    readonly_fields = ('created_at', 'updated_at')

    # Чтобы навыки (JSONField) красиво отображались структурой в форме редактирования
    fields = ('title', 'text', 'parsed_skills', 'created_at', 'updated_at')


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'url', 'created_at')
    list_display_links = ('title', 'company')
    list_filter = ('created_at', 'company')
    search_fields = ('title', 'company', 'description')
    readonly_fields = ('created_at',)


@admin.register(ResumeAdaptation)
class ResumeAdaptationAdmin(admin.ModelAdmin):
    # Выводим в список статусы и скоринг для наглядности
    list_display = ('get_user', 'resume', 'vacancy', 'status', 'score_before', 'score_after', 'created_at')
    list_display_links = ('resume', 'vacancy')

    # Фильтрация по статусам (pending, processing, success, failed) и базовая фильтрация по датам
    list_filter = ('status', 'created_at', 'score_after')

    # Поиск по автору резюме, названию вакансии и тексту
    search_fields = ('resume__user__username', 'vacancy__title', 'vacancy__company', 'adapted_text')

    # Защищаем системные поля от случайного ручного изменения в админке
    readonly_fields = ('created_at', 'updated_at')

    # Цветовое или текстовое оформление статуса в форме редактирования
    radio_fields = {'status': admin.HORIZONTAL}

    # Вспомогательный метод, чтобы вытащить имя пользователя в список отображения
    @admin.display(description="Кандидат")
    def get_user(self, obj):
        return obj.resume.user.username