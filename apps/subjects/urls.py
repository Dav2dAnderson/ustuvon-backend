from django.urls import path
from apps.subjects.views import (
    CategoryCreateView,
    CategoryDeleteView, CategoryUpdateView,
    SubjectCreateView, SubjectUpdateView,
    SubjectDeleteView, TaxonomyTreeView
)
app_name = 'subjects'

urlpatterns = [
    path('category_create', CategoryCreateView.as_view(), name='category_create'),
    path('category_update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category_delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delate'),
    path('subject_create/', SubjectCreateView.as_view(), name='subject_create'),
    path('subject_update/<int:pk>/', SubjectUpdateView.as_view(), name='subject_update'),
    path('subject_delete/<int:pk>/', SubjectDeleteView.as_view(), name='subject_delete'),
    path('taxanomy-tree/', TaxonomyTreeView.as_view({"get": "list"}), name='taxonomy-tree')
]