from django.urls import path
from apps.subjects.views import (
    CategoriesView, CategoryCreateView,
    CategoryDeleteView, CategoryUpdateView
)
app_name = 'subjects'

urlpatterns = [
    path('all', CategoriesView.as_view(), name='all-categories'),
    path('category_create', CategoryCreateView.as_view(), name='category_create'),
    path('category_update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category_delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delate')
]