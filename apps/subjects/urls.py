from django.urls import path
from apps.subjects.views import (
    CategoriesView, CategoryCreateView,
    CategoryDeleteView, CategoryUpdateView,
    SubjectCreateView, SubjectUpdateView,
    SubjectDeleteView, SubjectView
)
app_name = 'subjects'

urlpatterns = [
    path('all_categories/', CategoriesView.as_view(), name='all-categories'),
    path('category_create', CategoryCreateView.as_view(), name='category_create'),
    path('category_update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category_delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delate'),
    path('subject_create/', SubjectCreateView.as_view(), name='subject_create'),
    path('subject_update/<int:pk>/', SubjectUpdateView.as_view(), name='subject_update'),
    path('subject_delete/<int:pk>/', SubjectDeleteView.as_view(), name='subject_delete'),
    path('all_subjects/', SubjectView.as_view(), name='all_subjects'),
]