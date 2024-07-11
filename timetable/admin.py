from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Teacher)
admin.site.register(models.Class)
admin.site.register(models.Absence)
admin.site.register(models.ClassNeedsSub)
admin.site.register(models.Room)