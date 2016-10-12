from django.contrib import admin
from django.contrib.admin import AdminSite
from django.forms import TextInput, Textarea
from django.db import models

from .models import Teacher, CurrentClass, StudentRoster, AccountInfo, ReadingStats

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
                    'myonuser','myonpass')
    list_filter = ('kidsazteacher',)


class ReadingStatsAdmin(admin.ModelAdmin):
    list_display = ('student', 'starting_lexile', 'current_lexile', 'goal_lexile', 'myon_tests_taken',
                    'current_dra', 'goal_dra', 'myon_time_spent', 'myon_tests_taken', 'myon_books_finished',
                    'myon_books_opened')
    list_editable = ['goal_lexile', 'current_dra', 'goal_dra', 'starting_lexile']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '4'})},
        models.IntegerField: {'widget': TextInput(attrs={'size': '4'})},
    }





admin.site.register(StudentRoster, StudentRosterAdmin)
admin.site.register(Teacher)
admin.site.register(CurrentClass, CurrentClassAdmin)
admin.site.register(AccountInfo, AccountInfoAdmin)
admin.site.register(ReadingStats, ReadingStatsAdmin)


