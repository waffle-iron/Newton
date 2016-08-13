from django.conf.urls import url

from . import views

app_name = 'amc'

urlpatterns = [
    # /2016/2nd/Trost/input
    url(r'^(?i)(?P<year>20[0-9]{2})/(?P<grade>[a-z0-9]+)/(?P<teacher>[a-z0-9]+)/input$', views.input_amc_scores, name='inputamcscores'),
    # /2016/2nd/Trost
    url(r'^(?i)(?P<year>20[0-9]{2})/(?P<grade>[a-z0-9]+)/(?P<teacher>[a-z0-9]+)/?$', views.class_list, name='classlist'),
    # /2016
    url(r'^(?i)(?P<year>20[0-9]{2})/?$', views.school_roster, name='schoolroster'),
    url(r'^$', views.school_roster, name='schoolroster'),
]