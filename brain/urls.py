from django.conf.urls import url

from . import views

app_name = 'brain'

urlpatterns = [
    #url(r'^(?i)doctest/?$', views.generate_ixl_pdf, name='doctest'),
    #url(r'^(?i)printpdf/?$', views.print_pdf, name='printpdf'),
    # /16-17/    school roster
    url(r'^(?i)(?P<year>[0-9]{2}-[0-9]{2})/?$', views.school_roster, name='schoolroster'),
    # /16-17/2nd/   Grade List
    url(r'^(?i)(?P<year>[0-9]{2}-[0-9]{2})/(?P<grade>[a-z0-9]+)/?$', views.grade_list, name='gradelist'),
    # /16-17/2nd/trost/   Class List
    url(r'^(?i)(?P<year>[0-9]{2}-[0-9]{2})/(?P<grade>[a-z0-9]+)/(?P<teacher>[a-z0-9]+)/?$', views.class_list, name='classlist'),
    # /student/83   Student Detail
    url(r'^(?i)student/(?P<studentid>[0-9]+)/?$', views.student_detail, name='studentdetail'),

    url(r'^$', views.index, name='index'),

]
