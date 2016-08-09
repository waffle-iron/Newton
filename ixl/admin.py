from django.contrib import admin

# Register your models here.

from .models import IXLSkill, IXLSkillScores


class IXLSkillScoresAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'ixl_skill_id', 'date_recorded', 'score', )
    search_fields = ['student_id']

class IXLSkillAdmin(admin.ModelAdmin):
    list_display = ('skill_id', 'skill_description', 'ixl_url', 'category', )
    search_fields = ['skill_description', 'skill_id', 'category']


admin.site.register(IXLSkillScores, IXLSkillScoresAdmin)
admin.site.register(IXLSkill, IXLSkillAdmin)


