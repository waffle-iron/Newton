from django.contrib import admin
#from django.contrib.admin import AdminSite

from .models import Teacher, CurrentClass, StudentRoster, AccountInfo

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
    list_display = ('student', 'ixluser', 'ixlpass', 'kidsazuser','kidsazpass','myonuser','myonpass')
    list_filter = ('kidsazteacher',)


admin.site.register(StudentRoster, StudentRosterAdmin)
admin.site.register(Teacher)
admin.site.register(CurrentClass, CurrentClassAdmin)
admin.site.register(AccountInfo, AccountInfoAdmin)


