from django.contrib import admin

# Register your models here.

from .models import RITBand, NWEAScore, NWEASkill


admin.site.register(RITBand)
admin.site.register(NWEASkill)
admin.site.register(NWEAScore)
