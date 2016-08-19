from django.conf.urls import  include, url
from django.contrib import admin

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^(?i)admin/', include(admin.site.urls)),
    url(r'^(?i)amc/', include('amc.urls')),
    url(r'^(?i)nwea/', include('nwea.urls')),
    url(r'^(?i)classes/', include('brain.urls'), ),
    url(r'^(?i)ixl', include('ixl.urls')),
    # url(r'^(?i)eni/', include('eni.urls')),
    # url(r'^(?i)cba/', include('cba.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon/favicon.ico')),
    url(r'^', include('brain.urls'), ),
]

urlpatterns += staticfiles_urlpatterns()
