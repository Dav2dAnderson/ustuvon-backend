from rest_framework import serializers
from apps.subjects.models import Subject, Categories, Module, Topic

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

        category = Categories.objects.create(
            author=user,
            author_first_name = first_name,
            author_last_name = last_name,
            **validated_data
        )
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

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author_first_name = validated_data.get('author_first_name', instance.author_first_name)
        instance.author_last_name = validated_data.get('author_last_name', instance.author_last_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance 


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
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.author_first_name = validated_data.get('author_first_name', instance.author_first_name)
        instance.author_last_name = validated_data.get('author_last_name', instance.author_last_name)
        instance.save()
        return instance

class ModuleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
            'title',
            'subject'
        ]

    def create(self, validated_data):
        module = Module.objects.create(**validated_data)
        return module

class ModuleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
            'title',
            'subject',
            'is_active'
        ]

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

class TopicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = [
            'title',
            'module',
            'order',
            'is_active',
        ]

    def create(self, validated_data):
        topic = Topic.objects.create(**validated_data)
        return topic

class TopicUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = [
            'title',
            'module',
            'order',
            'is_active'
        ]

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.module = validated_data.get('module', instance.module)
        instance.order = validated_data.get('order', instance.order)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title', 'order']
class ModuleSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'order', 'topics']

class SubjectSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'title', 'description', 'modules']

class CategoryTreeSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Categories
        fields = ['id', 'title', 'subjects']