from django.contrib import admin
from dashboard.models import *
# Register your models here.


@admin.register(problem)
class problemAdmin(admin.ModelAdmin):
    ordering = ['-resolved','assignee']