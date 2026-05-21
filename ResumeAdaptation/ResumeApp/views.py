from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

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

        resume, vacancy = get_resume_and_vacancy(resume_id, vacancy_id, language)

        adaptation = run_resume_adaptation(resume, vacancy)

        response_serializer = ResumeAdaptationResponseSerializer(adaptation)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)