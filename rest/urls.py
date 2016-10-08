from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^missions$', views.get_all_missions, name='missions'),
    url(r'^missions/(?P<mission_id>[0-9]{1,5})/$', views.get_mission, name='missions'),
    url(r'^missions/(?P<id>[0-9]{1,5})/images/$', views.get_mission_images, name='missions'),
    url(r'^drones/$', views.get_drones, name='drones'),
    url(r'^drones/(?P<id>[0-9]{1,5})/$', views.get_drone, name='drones'),
    url(r'^drones/(?P<id>[0-9]{1,5})/control$', views.control_drone, name='drones'),
    url(r'^images/$', views.get_images, name='media'),
    url(r'^images/(?P<id>[0-9]{1,5})/$', views.get_image, name='media'),
    url(r'^images/current/$', views.get_current_image, name='media'),
    url(r'^images/missions/$', views.get_mission_images, name='media'),
    # url(r'^images/missions/(?P<id>[0-9]{1,5})/star/$', views.get_starred_images, name='media'),
]

