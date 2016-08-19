from django.contrib import admin

from .models import AMCTestResult, AMCTest


class AMCTestAdmin(admin.ModelAdmin):
    list_display = ('test_number','topic', 'name', 'grade_equivalent', 'total_questions', 'minimum_passing_grade',)
    ordering = ('test_number',)


class AMCTestResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'score', 'date_tested', 'passing_score')
    list_editable = ['score', 'test', 'date_tested']
    pass

admin.site.register(AMCTestResult, AMCTestResultAdmin)
admin.site.register(AMCTest, AMCTestAdmin)
