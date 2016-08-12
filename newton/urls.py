from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns =[
    url(r'^(?i)admin/', include(admin.site.urls)),
    url(r'^(?i)amc/', include('amc.urls')),
    url(r'^(?i)classes/', include('brain.urls'),),
    url(r'^(?i)ixl', include('ixl.urls')),
    #url(r'^(?i)eni/', include('eni.urls')),
    #url(r'^(?i)cba/', include('cba.urls')),

    url(r'^', include('brain.urls'),),

]

urlpatterns += staticfiles_urlpatterns()