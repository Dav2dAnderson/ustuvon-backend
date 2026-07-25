from django.shortcuts import get_object_or_404
from apps.subjects import serializer
from apps.subjects.serializer import (
    SubjectCreateSerializer,
    CategoriesCreateSerializer,
    CategoriesUpdateSerializer,
    SubjectUpdateSerializer,
    TopicCreateSerializer,
    TopicUpdateSerializer,
    ModuleCreateSerializer,
    ModuleUpdateSerializer,
    CategoryTreeSerializer
)
from apps.subjects.models import (
    Categories,
    Subject,
    Topic,
    Module,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

class TaxonomyTreeView(viewsets.ReadOnlyModelViewSet):
    queryset = Categories.objects.filter(is_active=True).prefetch_related(
        'subject__modules__topics'
    )
    serializer_class = CategoryTreeSerializer


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

class ModuleCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = ModuleCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "detail": "Something is wrong",
                "error": serializer.errors
            }, status=400)
        serializer.save()
        return Response({
            "detail": "Succesfully Created",
            "data": serializer.data
        }, status=201)
class ModuleUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, pk):
        module = get_object_or_404(Module, pk=pk)

        serializer = ModuleUpdateSerializer(instance=module, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response({
                "detail": "Something is wrong",
                "error": serializer.errors
            }, status=400)
        serializer.save()
        return Response({
            "detail": "Succesfully Updated",
            "data": serializer.data
        }, status=200)

class ModuleDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, pk):
        module = get_object_or_404(Module, pk=pk)

        if module:
            module.is_active = False
            module.save()
            return Response({
                "detail": "Succesfully deleted"
            }, status=200)
        else:
            return Response({
                "detail": "This module not found",
            }, status=400)

class TopicCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = TopicCreateSerializer(data=request.data)
        try:
            if not serializer.is_valid():
                return Response({
                    "detail": "Something is wrong",
                    "error": serializer.errors
                }, status=400)
            serializer.save()
            return Response({
                "detail": "Succesfully Created",
                "data": serializer.data
            }, status=201)
        except Exception as e:
            return f"error {e}"
        
class TopicUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk)

        serializer = TopicUpdateSerializer(instance=topic, data=request.data, partial=True)

        
        if not serializer.is_valid():
            return Response({
            "detail": "Something is wrong",
            "error": serializer.errors
            }, status=400)
        serializer.save()
        return Response({
        "detail": "Succesfully Updated",
        "data": serializer.data
        }, status=200)

class TopicDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def delete(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk)
    
        if topic:
            topic.is_active = False
            topic.save()
            return Response({
                "detail": "Succesfully deleted"
            }, status=200)
        else:
            return Response({
                "detail": "This module not found",
            }, status=400)