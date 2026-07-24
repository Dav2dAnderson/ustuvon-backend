from django.db import models
from apps.users.models import User

class Categories(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_first_name = models.CharField(max_length=100, blank=True, default="")
    author_last_name = models.CharField(max_length=100, blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"title {self.title}", f"author {self.author_first_name}, {self.author_last_name}"
    
class Subject(models.Model):
    title = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects', null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        if self.author:
            full_name = (
                f"{self.author.first_name} {self.author.last_name}".strip()
            )
            author_str = full_name if full_name else self.author.username
        else:
            author_str = "Muallif yo'q"

        return f"{self.title} - {author_str}"