from django.contrib import admin
from .models import Video
# Register your models here.

class VideoAdmin(admin.ModelAdmin):
    list_display = ('subject', 'title', 'shareurl','lesson_date')
    list_editable = ('title', 'shareurl', 'lesson_date')
    list_filter = ['subject','lesson_date']



admin.site.register(Video, VideoAdmin)