from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Resume, Vacancy
from .serializers.resume import ResumeSerializer, VacancySerializer
from .services import run_resume_adaptation, get_resume_and_vacancy
from .serializers import AdaptationRequestSerializer, ResumeAdaptationResponseSerializer


class AdaptResumeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AdaptationRequestSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        resume_id = serializer.validated_data['resume_id']
        vacancy_id = serializer.validated_data['vacancy_id']
        language = serializer.validated_data['language']

        resume, vacancy = get_resume_and_vacancy(resume_id, vacancy_id)

        adaptation = run_resume_adaptation(resume, vacancy, language)

        response_serializer = ResumeAdaptationResponseSerializer(adaptation)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ResumeAPIView(APIView):
    """Полный CRUD для резюме с использованием APIView"""
    permission_classes = [AllowAny]

    def get(self, request, resume_id=None):
        """GET: Получить список или конкретное резюме"""
        if resume_id:
            # Получить одно резюме
            resume = get_object_or_404(Resume, id=resume_id)
            serializer = ResumeSerializer(resume)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Получить список всех резюме
            resumes = Resume.objects.all()
            serializer = ResumeSerializer(resumes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """POST: Создать новое резюме"""
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, resume_id):
        """PUT: Полностью обновить резюме"""
        resume = get_object_or_404(Resume, id=resume_id)
        serializer = ResumeSerializer(resume, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, resume_id):
        """PATCH: Частично обновить резюме"""
        resume = get_object_or_404(Resume, id=resume_id)
        serializer = ResumeSerializer(resume, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, resume_id):
        """DELETE: Удалить резюме"""
        resume = get_object_or_404(Resume, id=resume_id)
        resume.delete()
        return Response(
            {"message": f"Резюме '{resume.title}' успешно удалено"},
            status=status.HTTP_204_NO_CONTENT
        )

class VacancyAPIView(APIView):
    """Полный CRUD для вакансий с использованием APIView"""
    permission_classes = [AllowAny]

    def get(self, request, vacancy_id=None):
        """GET: Получить список или конкретную вакансию"""
        if vacancy_id:
            vacancy = get_object_or_404(Vacancy, id=vacancy_id)
            serializer = VacancySerializer(vacancy)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            vacancies = Vacancy.objects.all()
            serializer = VacancySerializer(vacancies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """POST: Создать новую вакансию"""
        serializer = VacancySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, vacancy_id):
        """PUT: Полностью обновить вакансию"""
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        serializer = VacancySerializer(vacancy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, vacancy_id):
        """PATCH: Частично обновить вакансию"""
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        serializer = VacancySerializer(vacancy, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vacancy_id):
        """DELETE: Удалить вакансию"""
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        vacancy.delete()
        return Response(
            {"message": f"Вакансия '{vacancy.title}' успешно удалена"},
            status=status.HTTP_204_NO_CONTENT
        )