from django.urls import path

from .views import AdaptResumeAPIView, ResumeAPIView, VacancyAPIView

app_name = 'resume_app'

urlpatterns = [
    path('adapted-resume/', AdaptResumeAPIView.as_view(), name='resume-api'),
    path('resumes-all/', ResumeAPIView.as_view(), name='resume-all'),
    path('resumes-all/<int:resume_id>/', ResumeAPIView.as_view(), name='resume-detail-alt'),
    path('vacancies-all/', VacancyAPIView.as_view(), name='vacancy-all'),
    path('vacancies-all/<int:vacancy_id>/', VacancyAPIView.as_view(), name='vacancy-detail-alt'),
]