from django.contrib import admin

from .models import CommonCoreStateStandard, HomeworkCompletion




class CommonCoreStateStandardAdmin(admin.ModelAdmin):
    list_display = ('grade','domain','subdomain','topic','code','description')
    list_filter = ('domain', 'subdomain', )
    search_fields = ['grade', 'domain', 'subdomain', 'topic', 'code', 'description']

class HomeworkCompletionAdmin(admin.ModelAdmin):
    list_display = ['student', 'school_day', 'status']
    list_filter = [ 'status']
    list_editable = ['status',]

admin.site.register(CommonCoreStateStandard, CommonCoreStateStandardAdmin)
admin.site.register(HomeworkCompletion, HomeworkCompletionAdmin)

