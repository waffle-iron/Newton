from django.contrib import admin

from .models import CurrentAMCTest
# Register your models here.

class CurrentAMCTestAdmin(admin.ModelAdmin):
    pass

admin.site.register(CurrentAMCTest)
