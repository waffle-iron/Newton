from django.conf.urls import url

from . import views

app_name = 'parentletter'

urlpatterns = [
     url(r'(?i)print/$', views.school_roster, name='printgrade'),
     url(r'(?i)print/(?P<teacher>[a-z0-9\-]+)/$', views.class_roster, name='printclass'),

]