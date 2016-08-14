from django.contrib import admin

# Register your models here.

from .models import RITBand, NWEAScore, NWEASkill


class NWEASkillAdmin(admin.ModelAdmin):
    list_display = ('rit_band', 'skill', 'ixl_match',)
    list_filter = ['rit_band__domain','rit_band__subdomain', 'rit_band__rit_band']
    list_editable = ['ixl_match']

admin.site.register(RITBand)
admin.site.register(NWEASkill, NWEASkillAdmin)
admin.site.register(NWEAScore)
