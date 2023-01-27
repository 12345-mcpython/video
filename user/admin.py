from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Video)
admin.site.register(models.Role)
admin.site.register(models.TaskList)
admin.site.register(models.ExamineList)
admin.site.register(models.VideoPage)

# Register your models here.
