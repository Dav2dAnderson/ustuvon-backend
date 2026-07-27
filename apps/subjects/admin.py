from django.contrib import admin
from apps.subjects.models import Categories, Subject, Module, Topic
# Register your models here.
admin.site.register(Subject)
admin.site.register(Categories)
admin.site.register(Topic)
admin.site.register(Module)