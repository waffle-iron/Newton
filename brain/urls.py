from django.conf.urls import url

from . import views

app_name = 'brain'

urlpatterns = [
    # /2016/    school roster
    url(r'^(?i)(?P<year>20[0-9]{2})/?$', views.school_roster, name='schoolroster'),
    # /2016/2nd/   Grade List
    url(r'^(?i)(?P<year>20[0-9]{2})/(?P<grade>[a-z0-9]+)/?$', views.grade_list, name='gradelist'),
    # /2016/2nd/trost/   Class List
    url(r'^(?i)(?P<year>20[0-9]{2})/(?P<grade>[a-z0-9]+)/(?P<teacher>[a-z0-9]+)/?$', views.class_list, name='classlist'),
    # /student/83   Student Detail
    url(r'^(?i)student/(?P<studentid>[0-9]+)/?$', views.student_detail, name='studentdetail'),

    url(r'^$', views.index, name='index'),
]
