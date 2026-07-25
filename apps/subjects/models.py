from django.db import models
from apps.users.models import User

class Categories(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_first_name = models.CharField(max_length=100, blank=True, default="")
    author_last_name = models.CharField(max_length=100, blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.author and self.author_first_name:
            self.author_first_name = self.author_first_name
            self.author_last_name = self.author_last_name
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"title {self.title} | Muallif: {self.author_first_name}, {self.author_last_name}"
    
class Subject(models.Model):
    title = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects', null=True, blank=True)
    author_first_name = models.CharField(max_length=100, blank=True, default="")
    author_last_name = models.CharField(max_length=100, blank=True, default="")
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'subjects'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.author and not self.author_first_name:
            self.author_first_name = self.author.first_name
            self.author_last_name = self.author.last_name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"title: {self.title} | Muallif: {self.author_first_name}, {self.author_last_name}"

class Module(models.Model):
    title = models.CharField(max_length=150)
    subject =models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='modules')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'modules'
        ordering = ['-created_at']

    def __str__(self):
        return f"title: {self.title} | Subject: {self.subject}"

class Topic(models.Model):
    title = models.CharField(max_length=250)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='topics')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'topics'
        ordering = ['-created_at']

    def __str__(self):
        return f"title: {self.title} | Module: {self.module}"