from django.conf.urls import url

from . import views

app_name = 'badges'

urlpatterns = [
    # /log/45
     url(r'(?i)chooseavatar/(?P<student_id>[a-z0-9\-]+)$', views.choose_avatar, name='chooseavatar'),


    # # /level/D
    # url(r'(?i)/level/(?P<level>\w)$', views.level_detail, name='leveldetail'),
    # # /16-17/2nd/Trost
    # url(r'^(?i)/(?P<year>[0-9]{2}-[0-9]{2})/(?P<grade>[a-z0-9]+)/(?P<teacher>[a-z0-9\-]+)/?$', views.class_list, name='classlist'),

]