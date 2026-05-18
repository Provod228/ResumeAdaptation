from django.db import models

# Create your models here.



class Resume(models.Model):

    class Meta:
        verbose_name = "Обычное резюме"
        verbose_name_plural = "Обычные резюме"


class Vacancy(models.Model):

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"


class ResumeAdaptation(models.Model):


    class Meta:
        verbose_name = "Адаптированное резюме"
        verbose_name_plural = "Адаптированные резюме"