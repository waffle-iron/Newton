from django.conf.urls import url

from . import views

app_name = 'ixl'

urlpatterns = [
    # /skill/A-B.2
    url(r'(?i)/skill/(?P<skill_id>\w-\w\.\d+)$', views.skill_detail, name='skilldetail'),
    # /level/D
    url(r'(?i)/level/(?P<level>\w)$', views.level_detail, name='leveldetail'),
    # /2016/2nd/Trost
    url(r'^(?i)/(?P<year>20[0-9]{2})/(?P<grade>[a-z0-9]+)/(?P<teacher>[a-z0-9]+)/?$', views.class_list, name='classlist'),
    # /2016
    #url(r'^(?i)(?P<year>20[0-9]{2})/?$', views.skill_detail, name='skilldetail'),

    #url(r'^$', views.school_roster, name='schoolroster'),
]