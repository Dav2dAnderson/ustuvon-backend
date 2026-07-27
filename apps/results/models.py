from django.db import models

class UserTestResult(models.Model):
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"Result: {self.score}"