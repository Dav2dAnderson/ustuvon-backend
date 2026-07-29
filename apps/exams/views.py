from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from apps.exams.models import Question, Examination, Result
from apps.exams.serializer import (
    QuestionSerializer,
    ExaminationListSerializer,
    ExaminationDetailSerializer,
    ResultSerializer
)

class IsAdminOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff

class QuestionListView(APIView):
    permission_classes = [IsAuthenticated ,IsAdminOrReadOnly]

    def get(self, request):
        topic_id = request.query_params.get('topic')
        questions = Question.objects.select_related('topic').prefetch_related('options')

        if topic_id:
            questions = questions.filter(topic_id=topic_id)

        serializer = QuestionSerializer(questions.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class QuestionCreateView(APIView):
    permission_classes = [IsAuthenticated ,IsAdminOrReadOnly]

    def post(self, request):
        serializer = QuestionSerializer(data=request.data, context={'request': request})
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

class QuestionDeleteView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return Question.objects.prefetch_related('options').get(pk=pk)
        except Question.DoesNotExist:
            return None
    def delete(self, request, pk):
        question = self.get_object(pk)
        if not question:
            return Response({"detail": "Savol topilmadi"}, status=404)

        question.delete()
        return Response({"detail": "Savol muvaffaqiyatli o'chirildi"}, status=204)

class QuestionUpdateView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return Question.objects.prefetch_related('options').get(pk=pk)
        except Question.DoesNotExist:
            return None

    def get(self, request, pk):
        question = self.get_object(pk)
        if not question:
            return Response({"detail": "Savol topilmadi"}, status=404)

        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        question = self.get_object(pk)
        if not question:
            return Response({"detail": "Savol topilmadi"}, status=404)

        serializer = QuestionSerializer(question, data=request.data, partial=True, context={'request': request})
        if not serializer.is_valid():
            return Response({
                "detail": "Xatolik yuz berdi",
                "errors": serializer.errors
            }, status=400)

        serializer.save()
        return Response({
            "detail": "Savol muvaffaqiyatli yangilandi",
            "data": serializer.data
        }, status=200)

class ExaminationListCreateView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        test_type = request.query_params.get('test_type')
        exams = Examination.objects.filter(is_active=True).prefetch_related('questions')

        if test_type:
            exams = exams.filter(test_type=test_type)

        serializer = ExaminationListSerializer(exams, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = ExaminationDetailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "detail": "Xatolik yuz berdi",
                "errors": serializer.errors
            }, status=400)

        serializer.save()
        return Response({
            "detail": "Imtihon muvaffaqiyatli yaratildi",
            "data": serializer.data
        }, status=201)

class ExaminationDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return Examination.objects.prefetch_related('questions__options').get(pk=pk, is_active=True)
        except Examination.DoesNotExist:
            return None

    def get(self, request, pk):
        exam = self.get_object(pk)
        if not exam:
            return Response({"detail": "Imtihon topilmadi yoki faol emas"}, status=404)
        if not request.user.is_staff:
            has_taken = Result.objects.filter(user=request.user, exam=exam).exists()
            if has_taken:
                return Response(
                    {"detail": "Siz ushbu imtihonni allaqachon topshirib bo'lgansiz!"},
                    status=403
                )

        serializer = ExaminationDetailSerializer(exam)
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        exam = self.get_object(pk)
        if not exam:
            return Response({"detail": "Imtihon topilmadi"}, status=404)

        serializer = ExaminationDetailSerializer(exam, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({
                "detail": "Xatolik yuz berdi",
                "errors": serializer.errors
            }, status=400)

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

        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ResultSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({
                "detail": "Xatolik yuz berdi",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user)
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
            return Response({"detail": "Natija topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ResultSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response({"detail": "Ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)

        result = self.get_object(pk, request.user)
        if not result:
            return Response({"detail": "Natija topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        result.delete()
        return Response({"detail": "Natija o'chirildi"}, status=status.HTTP_204_NO_CONTENT)