from django.contrib import admin
from apps.subjects.models import Categories, Subject
# Register your models here.
admin.site.register(Subject)
admin.site.register(Categories)