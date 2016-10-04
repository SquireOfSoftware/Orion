from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^missions/$', views.get_all_missions, name='missions'),
    url(r'^missions/(?P<id>[0-9]{1,5})/$', views.get_mission, name='missions'),
    url(r'^drones', views.drones, name='drones'),
    url(r'^media', views.media, name='media'),
]

