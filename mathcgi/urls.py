from django.conf.urls import url

from . import views

app_name = 'mathcgi'

urlpatterns = [
#
#
# # Portal URLS
    url(r'^(?i)(?P<year>[0-9]{2}-[0-9]{2})/(?P<grade>[a-z0-9]+)/(?P<teacher>[a-z0-9\-]+)/input?$', views.input_cgi, name='inputcgi'),
    url(r'^(?i)(?P<year>[0-9]{2}-[0-9]{2})/(?P<grade>[a-z0-9]+)/(?P<teacher>[a-z0-9\-]+)/print?$', views.print_cgi, name='printcgi'),

    #     url(r'^(?i)portal/(?P<grade>[a-z0-9]+)/(?P<teacher>[a-z0-9\-]+)/?$', views.portal_class, name='portalclass'),
#     url(r'^(?i)portal/(?P<grade>[a-z0-9]+)/(?P<teacher>[a-z0-9\-]+)/(?P<studentid>[0-9]+)/?$', views.portal_student, name='portalstudent'),
#     url(r'^(?i)portal/(?P<grade>[a-z0-9]+)/(?P<teacher>[a-z0-9\-]+)/groups/?$', views.make_groups, name='makegroups'),
#     url(r'^(?i)portal/(?P<grade>[a-z0-9]+)/(?P<teacher>[a-z0-9\-]+)/morning/?$', views.morning_message, name='morningmessage'),
#     url(r'^(?i)portal/(?P<grade>[a-z0-9]+)/(?P<teacher>[a-z0-9\-]+)/random/?$', views.random_student,
#         name='randomstudent'),
#
#     url(r'^$', views.index, name='index'),
#
]
