from django.contrib import admin
from apps.exams.models import (
    Question, 
    Topic,
    Option,
    Examination,
    Result
)
# Register your models here.

admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Topic)
admin.site.register(Examination)
admin.site.register(Result)