from django.contrib import admin

from .models import AMCTestResult, AMCTestDay, AMCTest

# Register your models here.


class AMCAdmin(admin.TabularInline):
    #list_display = ('student', 'test', 'score', )
    #list_filter = ['student', 'test', 'score', ]
    model = AMCTestResult
    extra = 10


class AMCTestDayAdmin(admin.ModelAdmin):
    inlines = [AMCAdmin]
    #list_display = ('student', 'test', 'score', 'date_taken',)
    #list_filter = ['student', 'test', 'score', 'date_taken',]

class AMCTestAdmin(admin.ModelAdmin):
    list_display = ('test_number','topic', 'name', 'grade_equivalent', 'total_questions', 'minimum_passing_grade',)
    ordering = ('test_number',)


class AMCTestResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'score', 'date_taken')
    list_editable = ['score', 'test', 'date_taken']

admin.site.register(AMCTestResult, AMCTestResultAdmin)
admin.site.register(AMCTestDay, AMCTestDayAdmin)
admin.site.register(AMCTest, AMCTestAdmin)
