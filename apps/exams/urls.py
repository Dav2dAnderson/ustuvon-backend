from django.urls import path
from .views import (
    QuestionListCreateView, QuestionDetailView,
    ExaminationListCreateView, ExaminationDetailView,
    ResultListCreateView, ResultDetailView
)

urlpatterns = [
    path('questions/', QuestionListCreateView.as_view()),
    path('questions/<int:pk>/', QuestionDetailView.as_view()),
    path('examinations/', ExaminationListCreateView.as_view()),
    path('examinations/<int:pk>/', ExaminationDetailView.as_view()),
    path('results/', ResultListCreateView.as_view()),
    path('results/<int:pk>/', ResultDetailView.as_view()),
]