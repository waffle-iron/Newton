from django.contrib import admin
from django.contrib.admin import AdminSite
from django.forms import TextInput, Textarea
from django.db import models

from .models import Teacher, CurrentClass, StudentRoster, AccountInfo, \
    ReadingStats, MorningMessage, MorningMessageSettings, Subject, Schedule


'''
class BrainAdminSite(AdminSite):
    site_header = 'Newton Administration'
'''
admin.site.site_title = 'Newton Administration'
admin.site.site_header = 'Newton Administration'


class StudentRosterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['first_name', 'last_name', 'current_class']}),
        ('Extra Details', {'fields': ['date_of_birth', 'gender', 'email']}),
    ]
    list_display = ('first_name', 'last_name', 'current_class', 'gender', 'date_of_birth', )
    list_filter = ['current_class', 'gender', ]
    radio_fields = {'gender': admin.HORIZONTAL}
    search_fields = ['first_name', 'last_name',]


class StudentInline(admin.TabularInline):
    model = StudentRoster
    extra = 3


class CurrentClassAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'grade', 'year',)
    list_filter = ['grade', 'year',]
    inlines = [StudentInline]

class AccountInfoAdmin(admin.ModelAdmin):
    list_display = ('student', 'ixluser', 'ixlpass', 'kidsazteacher', 'kidsazuser','kidsazpass',
                    'myonuser','myonpass', 'videos', 'readworkscode')
    list_filter = ('student__current_class__teacher','student__current_class__grade',)
    list_editable = ['ixlpass', 'kidsazpass', 'myonpass', 'myonuser', 'videos', 'readworkscode']
    search_fields = ['ixluser', 'myonuser', 'kidsazteacher', 'student__first_name', 'student__last_name']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '10'})},
        models.IntegerField: {'widget': TextInput(attrs={'size': '10'})},
    }


class ReadingStatsAdmin(admin.ModelAdmin):
    list_display = ('student', 'starting_lexile', 'current_lexile', 'goal_lexile', 'lexile_progress', 'myon_tests_taken',
                    'starting_dra','current_dra', 'goal_dra', 'myon_time_spent', 'myon_tests_taken', 'myon_books_finished',
                    'myon_books_opened')
    list_editable = ['goal_lexile', 'current_dra', 'goal_dra', 'starting_dra']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '4'})},
        models.IntegerField: {'widget': TextInput(attrs={'size': '4'})},
    }
    search_fields = ['student__first_name', 'student__last_name']
    list_filter = ['student__current_class__teacher']

class SpecialScheduleAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    list_editable = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']


class MorningMessageAdmin(admin.ModelAdmin):
    list_display = ['teacher','date','message']
    list_editable = ['date','message']
    list_filter = ['teacher']

# class MorningMessageSettingsAdmin(admin.ModelAdmin):
#     list_display = ['teacher', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']
#     list_editable = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'day', 'subject1', 'subject2', 'subject3', 'subject4', 'subject5', 'subject6','subject7',)
    list_editable = ( 'day', 'subject1', 'subject2', 'subject3', 'subject4', 'subject5', 'subject6','subject7',)
    list_filter = ('teacher', 'day', )


admin.site.register(StudentRoster, StudentRosterAdmin)
admin.site.register(Teacher)
admin.site.register(CurrentClass, CurrentClassAdmin)
admin.site.register(AccountInfo, AccountInfoAdmin)
admin.site.register(ReadingStats, ReadingStatsAdmin)
admin.site.register(MorningMessage, MorningMessageAdmin)
admin.site.register(MorningMessageSettings,)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Schedule, ScheduleAdmin)

