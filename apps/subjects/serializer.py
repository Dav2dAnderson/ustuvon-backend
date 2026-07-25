from unicodedata import category

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
        fields = [
            'title',
            'is_active',
            'created_at',
            'author_last_name',
            'author_first_name'
        ]

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
        fields = [
            'title',
            'is_active',
            'author_last_name',
            'author_first_name'
        ]

class CreateSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'title',
            'category',
            'description',
            'author_first_name',
            'author_last_name'
        ]

    def create(self, validated_data):
        return super().create(validated_data)

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class SubjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'title',
            'category',
            'description',
            'author_first_name',
            'author_last_name',
        ]

    def validate_title(self, value):
        if Subject.objects.filter(title=value).exists():
            raise serializers.ValidationError("This Subject title already exits")
        return value
    def validate_category(self, value):
        if not Categories.objects.filter(category=value).exists():
            raise serializers.ValidationError("This Category does not exist")

        return value
    def create(self, validated_data):
        subject = Subject.objects.create(**validated_data)
        return subject

class SubjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'title',
            'category',
            'description',
            'author_first_name',
            'author_last_name',
            'is_active'
        ]
    def validate_title(self, value):
        if Subject.objects.filter(title=value).exists():
            raise serializers.ValidationError(
                'This Subject title already exits'
            )
        return value
    def validate_category(self, value):
        if not Subject.objects.filter(category=value).exists():
            raise serializers.ValidationError(
                'This Category does not exits'
            )
        return value
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title),
        instance.category = validated_data.get('category', instance.category),
        instance.description = validated_data.get('description', instance.description),
        instance.author_first_name = validated_data.get('author_first_name', instance.author_first_name),
        instance.author_last_name = validated_data.get('author_last_name', instance.author_last_name),
        instance.save()