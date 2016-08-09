from django.conf.urls import url

from . import views


#
app_name = 'amc'


urlpatterns = [

    # /2016/2nd/Trost/
    url(r'^(?i)(?P<year>20[0-9]{2})/(?P<grade>[a-z0-9]+)/(?P<teacher>[a-z0-9]+)/?$', views.input_amc_scores, name='inputamcscores'),

    url(r'^$', views.amc_index, name='index'),
]