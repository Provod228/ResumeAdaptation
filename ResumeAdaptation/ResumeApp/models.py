from django.db import models

# Create your models here.


class Resume(models.Model):
    # user = models.ForeignKey(
    #     'UserApp.User',
    #     on_delete=models.CASCADE,
    #     related_name='resumes',
    #     verbose_name="Пользователь"
    # )
    title = models.CharField(
        max_length=255,
        default="Мое резюме",
        verbose_name="Название резюме",
        help_text="Например: Python-разработчик"
    )
    text = models.TextField(
        blank=True,
        verbose_name="Текст резюме",
        help_text="Полный исходный текст резюме"
    )

    # Сюда складываем навыки, извлеченные из резюме для последующего скоринга
    parsed_skills = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Выделенные навыки из резюме",
        help_text="Ключевые навыки, которые NLP/LLM нашли в исходном тексте"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    def __str__(self):
        # Временно убираем упоминание self.user, пока нет пользователей
        return self.title

    class Meta:
        verbose_name = "Обычное резюме"
        verbose_name_plural = "Обычные резюме"
        ordering = ['-created_at']


class Vacancy(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название вакансии",
        help_text="Например: Python-разработчик"
    )
    company = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Компания"
    )
    description = models.TextField(
        verbose_name="Полное описание вакансии",
        help_text="Вставленный текст вакансии или результат парсинга"
    )
    url = models.URLField(
        blank=True,
        verbose_name="Ссылка на вакансию",
        help_text="Ссылка на hh.ru, LinkedIn и т.д."
    )

    # Ключевое поле для NLP/LLM: сюда складываем выделенные навыки/требования
    parsed_skills = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Выделенные навыки",
        help_text="Список ключевых слов и требований, извлеченных из вакансии"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.title} в {self.company}" if self.company else self.title

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"


class ResumeAdaptation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В очереди'),
        ('processing', 'Адаптируется'),
        ('success', 'Успешно готово'),
        ('failed', 'Ошибка'),
    ]

    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('en', 'Английский'),
    ]

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='ru',
        verbose_name="Язык вывода",
        help_text="Язык, на котором будет составлено адаптированное резюме"
    )

    resume = models.ForeignKey(
        'Resume',
        on_delete=models.CASCADE,
        related_name='adaptations',
        verbose_name="Исходное резюме"
    )
    vacancy = models.ForeignKey(
        'Vacancy',
        on_delete=models.CASCADE,
        related_name='adaptations',
        verbose_name="Вакансия"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус адаптации"
    )

    # Результат работы LLM
    adapted_text = models.TextField(
        blank=True,
        verbose_name="Адаптированный текст резюме"
    )

    # Метрики для ATS-фильтров и скоринга
    score_before = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Совпадение ДО (%)",
        help_text="Процент совпадения исходного резюме с вакансией"
    )
    score_after = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Совпадение ПОСЛЕ (%)",
        help_text="Процент совпадения после адаптации"
    )

    # Лог изменений (что именно LLM переписала или добавила)
    changes_log = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Лог изменений",
        help_text="Данные о том, какие навыки были добавлены или изменены"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата адаптации")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Адаптация для {self.vacancy.title}"

    class Meta:
        verbose_name = "Адаптированное резюме"
        verbose_name_plural = "Адаптированные резюме"
