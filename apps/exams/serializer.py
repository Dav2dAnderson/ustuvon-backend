from rest_framework import serializers
from apps.subjects.models import Topic
from .models import Examination, Question, Option, Result, Difficulty, TestType


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct', 'image']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False)
    topic_title = serializers.ReadOnlyField(source='topic.title')

    class Meta:
        model = Question
        fields = [
            'id',
            'topic',
            'topic_title',
            'text',
            'difficulty',
            'passage_text',
            'audio_file',
            'image',
            'options',
            'created_at'
        ]

    def validate(self, attrs):
        request = self.context.get('request')
        options_data = self.initial_data.get('options', [])
        if request and request.method in ['POST', 'PUT']:
            if len(options_data) < 2:
                raise serializers.ValidationError({
                    "options": "Savolda kamida 2 ta variant bo'lishi shart."
                })

            correct_answers = [opt for opt in options_data if opt.get('is_correct') is True]
            if len(correct_answers) == 0:
                raise serializers.ValidationError({
                    "options": "Variantlar orasida kamida 1 ta to'g'ri javob (is_correct=True) ko'rsatilsin."
                })

        return attrs


class ExaminationListSerializer(serializers.ModelSerializer):
    questions_count = serializers.IntegerField(source='questions.count', read_only=True)

    class Meta:
        model = Examination
        fields = [
            'id',
            'title',
            'test_type',
            'duration_time',
            'transition_assessment',
            'questions_count',
            'is_active',
            'created_at'
        ]


class ExaminationDetailSerializer(serializers.ModelSerializer):
    """Test haqida to'liq ma'lumot va savollarni chiqarish/yaratish uchun serializer"""
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Examination
        fields = [
            'id',
            'title',
            'test_type',
            'duration_time',
            'transition_assessment',
            'instruction_audio',
            'questions',
            'is_active',
            'created_at'
        ]

    def validate_duration_time(self, value):
        if value < 5 or value > 360:
            raise serializers.ValidationError("Test vaqti 5 va 360 daqiqa oralig'ida bo'lishi kerak.")
        return value

    def validate_transition_assessment(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("O'tish bali 0 va 100 oralig'ida bo'lishi kerak.")
        return value


class ResultSerializer(serializers.ModelSerializer):
    user_full_name = serializers.ReadOnlyField(source='user.get_full_name')
    exam_title = serializers.ReadOnlyField(source='exam.title')

    class Meta:
        model = Result
        fields = [
            'id',
            'user',
            'user_full_name',
            'exam',
            'exam_title',
            'score',
            'is_passed',
            'completed_at'
        ]
        read_only_fields = ['user', 'is_passed', 'completed_at']

    def validate_score(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("To'plangan ball 0 va 100 oralig'ida bo'lishi shart.")
        return value

    def validate(self, attrs):
        request = self.context.get('request')
        exam = attrs.get('exam')

        if request and request.user and exam:
            if not request.user.is_staff:
                already_taken = Result.objects.filter(user=request.user, exam=exam).exists()
                if already_taken:
                    raise serializers.ValidationError({
                        "exam": "Siz ushbu imtihonni topshirib bo'lgansiz. Qayta topshirish taqiqlangan!"
                    })
        return attrs