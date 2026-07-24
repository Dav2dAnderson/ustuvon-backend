from rest_framework import serializers
from apps.subjects.models import Subject, Categories

class CategoriesSerializer(serializers.ModelSerializer):
    author_first_name = serializers.ReadOnlyField(
        source='author.first_name', default=""
    )
    author_last_name = serializers.ReadOnlyField(
        source='author.last_name', default=""
    )

    class Meta:
        model = Categories
        fields = ['title', 'is_active', 'created_at', 'author_last_name', 'author_first_name']

class CategoriesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = [
            "id",
            "title",
            "author_first_name",
            "author_last_name",
            "created_at",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request and request.user.is_authenticated else None

        first_name = validated_data.get("author_first_name")
        last_name = validated_data.get("author_last_name")

        if user:
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            user.save()

        category = Categories.objects.create(author=user, **validated_data)
        return category
    
class CategoriesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['title', 'is_active', 'author_last_name', 'author_first_name']

class CreateSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['title', 'category', 'description', 'author_first_name', 'author_last_name']

    def create(self, validated_data):
        return super().create(validated_data)

class SubjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['title', 'category', 'description', 'author_first_name', 'author_last_name']
