from django.conf.urls import url

from . import views

app_name = 'amc'

urlpatterns = [
    # /16-17/2nd/Trost/input
    url(r'^(?i)(?P<year>[0-9]{2}-[0-9]{2})/(?P<grade>[a-z0-9]+)/(?P<teacher>[a-z0-9]+)/input$', views.input_amc_scores, name='inputamcscores'),
    # /16-17/2nd/Trost
    url(r'^(?i)(?P<year>[0-9]{2}-[0-9]{2})/(?P<grade>[a-z0-9]+)/(?P<teacher>[a-z0-9]+)/?$', views.class_list, name='classlist'),
    # /16-17
    url(r'^(?i)(?P<year>[0-9]{2}-[0-9]{2})/?$', views.school_roster, name='schoolroster'),
    url(r'^$', views.school_roster, name='schoolroster'),
]