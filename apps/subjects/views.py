from django.shortcuts import get_object_or_404
from pygments.styles import nord

from apps.subjects.serializer import (SubjectCreateSerializer,
                                      CategoriesCreateSerializer,
                                      CategoriesUpdateSerializer,
                                      CategoriesSerializer,
                                      SubjectUpdateSerializer, SubjectSerializer)
from apps.subjects.models import Categories, Subject
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class DynamicPageSizePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = (
        "page_size"
    )
    max_page_size = 100

class CategoriesView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CategoriesSerializer
    pagination_class = DynamicPageSizePagination

    def get(self, request):
        categories = Categories.objects.all().select_related("author").all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(categories, request, view=self)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data, status=200)

class CategoryCreateView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = CategoriesCreateSerializer

    def post(self, request):
        seralizer = self.serializer_class(data=request.data)

        if not seralizer.is_valid():
            return Response({
                "detail": "Something is Wrong",
                "error": seralizer.errors
            }, status=400)
        seralizer.save(author=request.user)

        return Response({
            "detail": "Succesfully  Created",
            "data": seralizer.data
        }, status=201)

class CategoryUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CategoriesUpdateSerializer

    def patch(self,request, pk):

        category = get_object_or_404(Categories, pk=pk)

        serializer = self.serializer_class(partial=True, data=request.data, instance = category)

        if not serializer.is_valid():
            return Response({
                "detail": "Something is wrong",
                "error": serializer.errors
            }, status=400)
        serializer.save(author=request.user)

        return Response({
            "detail": "Succesfully Updated",
            "data": serializer.data
        }, status=200)

class CategoryDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, pk):
        category = get_object_or_404(Categories, pk=pk)
        if category:
            category.is_active = False
            category.save()
            return Response({
                "detail": "Category succesfully deleted"
            }, status=200)
        return Response({"detail": "This category is not found"}, status=204)

class SubjectView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = SubjectSerializer
    pagination_class = DynamicPageSizePagination

    def get(self,request):
        subjects = Subject.objects.all().select_related("author").all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(subjects, request, view=self)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = self.serializer_class(subjects, many=True)
        return Response(serializer.data, status=200)

class SubjectCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = SubjectCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({
                "detail": "Succesfully  Created",
                "data": serializer.data
            }, status=201)
        else:
            return Response({
                "detail": "Something is wrong",
                "error": serializer.errors
            }, status=400)

class SubjectUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = SubjectUpdateSerializer

    def patch(self, request, pk):
        subject = get_object_or_404(Subject, pk=pk)

        serializer = self.serializer_class(partial=True, data=request.data, instance=subject)

        if not serializer.is_valid():
            return Response({
                "detail": "Something is wrong",
                'error': serializer.errors
            }, status=400)
        serializer.save(author=request.user)
        return Response({
            "detail": "Succesfully  Updated",
            "data": serializer.data
        }, status=200)

class SubjectDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, pk):
        subject = get_object_or_404(Subject, pk=pk)

        if subject:
            subject.is_active = False
            subject.save()
        else:
            return Response({
                "detail": "This subject is not found"
            }, status=404)