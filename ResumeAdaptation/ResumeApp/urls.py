from django.urls import path

from .views import AdaptResumeAPIView

app_name = 'resume_app'

urlpatterns = [
    path('adapted-resume/', AdaptResumeAPIView.as_view(), name='resume-api'),
]