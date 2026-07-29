from django.db import models
from apps.subjects.models import Topic
from apps.users.models import User

class TestType(models.TextChoices):
    IELTS = 'IELTS', 'IELTS'
    DTM = 'DTM', 'DTM'
    SAT = 'SAT', 'SAT'
    MILLIY = 'MILLIY', 'Milliy Sertifikat'

class Difficulty(models.TextChoices):
    EASY = 'easy', 'Easy'
    MIDDLE = 'middle', 'Middle'
    HARD = 'hard', 'Hard'

class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices, default=Difficulty.EASY)
    passage_text = models.TextField(null=True, blank=True, help_text="Reading text matni")
    audio_file = models.FileField(upload_to='questions/audio/', null=True, blank=True)
    image = models.ImageField(upload_to='questions/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'questions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.topic.title} | {self.text[:30]}..."

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    image = models.ImageField(upload_to='options/images/', null=True, blank=True)

    class Meta:
        db_table = 'options'

    def __str__(self):
        return f"{self.text} ({'To-gri' if self.is_correct else 'Noto`gri'})"

class Examination(models.Model):
    title = models.CharField(max_length=200)
    test_type = models.CharField(max_length=20, choices=TestType.choices, default=TestType.DTM)
    duration_time = models.PositiveIntegerField(default=120, help_text="Test davomiyligi (daqiqada)")
    transition_assessment = models.FloatField(default=56.7)
    questions = models.ManyToManyField(Question)
    instruction_audio = models.FileField(upload_to='exams/instructions/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'examinations'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.test_type}] {self.title}, ({self.duration_time} min)"

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name='results')
    score = models.FloatField()
    is_passed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'results'
        ordering = ['-completed_at']

    def save(self, *args, **kwargs):
        self.is_passed = self.score >= self.exam.transition_assessment
        super().save(*args, **kwargs)