from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.exams.models import Question, Option, Examination, Result
from apps.exams.serializer import (
    QuestionCreateSerializer, QuestionListSerializer, QuestionUpdateSerializer,
    ExaminationCreateSerializer, ExaminationListSerializer, ExaminationDetailSerializer,
    ResultCreateSerializer, ResultListSerializer
)

class QuestionListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        questions = Question.objects.select_related('topic').prefetch_related('options').all()
        serializer = QuestionListSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = QuestionCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "detail": "Xatolik yuz berdi",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "detail": "Savol muvaffaqiyatli yaratildi",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


class QuestionDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, pk):
        try:
            return Question.objects.prefetch_related('options').get(pk=pk)
        except Question.DoesNotExist:
            return None

    def get(self, request, pk):
        question = self.get_object(pk)
        if not question:
            return Response({"detail": "Savol topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionListSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        question = self.get_object(pk)
        if not question:
            return Response({"detail": "Savol topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionUpdateSerializer(question, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({
                "detail": "Xatolik yuz berdi",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "detail": "Savol muvaffaqiyatli yangilandi",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        question = self.get_object(pk)
        if not question:
            return Response({"detail": "Savol topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        question.delete()
        return Response({"detail": "Savol muvaffaqiyatli o'chirildi"}, status=status.HTTP_204_NO_CONTENT)

class ExaminationListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        exams = Examination.objects.prefetch_related('questions').all()
        serializer = ExaminationListSerializer(exams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ExaminationCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "detail": "Xatolik yuz berdi",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "detail": "Imtihon muvaffaqiyatli yaratildi",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


class ExaminationDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, pk):
        try:
            return Examination.objects.prefetch_related('questions__options').get(pk=pk)
        except Examination.DoesNotExist:
            return None

    def get(self, request, pk):
        exam = self.get_object(pk)
        if not exam:
            return Response({"detail": "Imtihon topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ExaminationDetailSerializer(exam)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        exam = self.get_object(pk)
        if not exam:
            return Response({"detail": "Imtihon topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ExaminationCreateSerializer(exam, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({
                "detail": "Xatolik yuz berdi",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "detail": "Imtihon muvaffaqiyatli yangilandi",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        exam = self.get_object(pk)
        if not exam:
            return Response({"detail": "Imtihon topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        exam.delete()
        return Response({"detail": "Imtihon muvaffaqiyatli o'chirildi"}, status=status.HTTP_204_NO_CONTENT)

class ResultListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            results = Result.objects.select_related('user', 'exam').all()
        else:
            results = Result.objects.select_related('exam').filter(user=request.user)
        serializer = ResultListSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ResultCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response({
                "detail": "Xatolik yuz berdi",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "detail": "Natija muvaffaqiyatli saqlandi",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


class ResultDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            if user.is_staff:
                return Result.objects.select_related('user', 'exam').get(pk=pk)
            return Result.objects.select_related('exam').get(pk=pk, user=user)
        except Result.DoesNotExist:
            return None

    def get(self, request, pk):
        result = self.get_object(pk, request.user)
        if not result:
            return Response({"detail": "Natija topilmadi"}, status=404)
        serializer = ResultListSerializer(result)
        return Response(serializer.data, status=200)

    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response({"detail": "Ruxsat yo'q"}, status=403)
        result = self.get_object(pk, request.user)
        if not result:
            return Response({"detail": "Natija topilmadi"}, status=404)
        result.delete()
        return Response({"detail": "Natija o'chirildi"}, status=204)