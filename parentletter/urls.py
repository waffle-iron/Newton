from django.conf.urls import url

from . import views

app_name = 'parentletter'

urlpatterns = [
     url(r'(?i)print/$', views.school_roster, name='printgrade'),

]