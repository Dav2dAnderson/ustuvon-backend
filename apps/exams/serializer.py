from rest_framework import serializers
from .models import Difficulty, Question, Option, Examination, Result

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']

class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'topic', 'text', 'difficulty', 'options']

    def validate_options(self, value):
        if len(value) < 4:
            raise serializers.ValidationError('4 ta variant bo`lishi shart')

        correct = [o for o in value if o.get('is_correct')]
        if len(correct) != 1:
            raise serializers.ValidationError('Kamida faqat bitta javob bo`lishi kerak')
        return value

    def create(self, validated_data):
        options_data = validated_data.pop('is_correct')
        question = Question.objects.create(**validated_data)
        Option.objects.bulk_create([
            Option(question=question, **option) for option in options_data
        ])
        return question

class QuestionListSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    difficulty = serializers.CharField(source='get_difficulty_display')

    class Meta:
        model = Question
        fields = ['id', 'topic', 'text', 'difficulty', 'options', 'created_at']

class QuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text', 'difficulty', 'topic']

class ExaminationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examination
        fields = ['id', 'title', 'duration_time', 'transition_assessment', 'questions', 'is_active']

    def validate_questions(self, value):
        if len(value) == 0:
            raise serializers.ValidationError('Kamida bitta savol bo`lishi kerak')
        return value

    def validate_transition_assessment(self, attrs):
        if not (0 <= attrs <= 100):
            raise serializers .ValidationError("O`tish bali 0 dan 100 gacha bo`lishi shart")
        return attrs

class ExaminationListSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Examination
        fields = ['id', 'title', 'duration_time', 'transition_assessment', 'questions_count', 'is_active', 'created_at']

    def get_questions_count(self, obj):
        return obj.questions.count()


class ExaminationDetailSerializer(serializers.ModelSerializer):
    questions = QuestionListSerializer(many=True, read_only=True)

    class Meta:
        model = Examination
        fields = ['id', 'title', 'duration_time', 'transition_assessment', 'questions', 'is_active', 'created_at']


class ResultCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['id', 'exam', 'score']

    def validate_score(self, value):
        if not (0 <= value <= 100):
            raise serializers.ValidationError("Score 0 dan 100 gacha bo'lishi kerak")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return Result.objects.create(**validated_data)


class ResultListSerializer(serializers.ModelSerializer):
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Result
        fields = ['id', 'user_email', 'exam_title', 'score', 'is_passed', 'completed_at']