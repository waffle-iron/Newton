from django.contrib import admin

# Register your models here.

from .models import IXLSkill, IXLSkillScores, IXLStats, Challenge, ChallengeAssignment


class IXLSkillScoresAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'ixl_skill_id', 'date_recorded', 'score', )
    search_fields = ['student_id']

class IXLSkillAdmin(admin.ModelAdmin):
    list_display = ('skill_id', 'skill_description', 'ixl_url', 'category', )
    search_fields = ['skill_description', 'skill_id', 'category']

class IXLStatsAdmin(admin.ModelAdmin):
    list_display = ('student', 'last_practiced', 'questions_answered', 'time_spent')


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', )
    # search_fields = ['student_id']


class ChallengeAssignmentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'challenge', 'date_assigned', 'current_challenge', 'complete')


admin.site.register(IXLSkillScores, IXLSkillScoresAdmin)
admin.site.register(IXLSkill, IXLSkillAdmin)
admin.site.register(IXLStats, IXLStatsAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(ChallengeAssignment, ChallengeAssignmentAdmin)

