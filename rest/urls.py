from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^missions/?$', views.handle_missions),
    url(r'^missions/(?P<mission_id>[0-9]{1,5})/?$', views.get_mission),
    url(r'^missions/(?P<mission_id>[0-9]{1,5})/start?$', views.start_mission),
    url(r'^missions/(?P<id>[0-9]{1,5})/images/?$', views.get_mission_images),
    url(r'^drones/?$', views.handle_drones),
    url(r'^drones/(?P<drone_id>[0-9]{1,5})/?$', views.get_drone),
    url(r'^drones/(?P<drone_id>[0-9]{1,5})/control/?$', views.control_drone),
    url(r'^images/?$', views.get_images),
    url(r'^images/(?P<image_id>[0-9]{1,5})/?$', views.get_image),
    url(r'^images/current/?$', views.get_current_image),
    url(r'^images/missions/?$', views.get_mission_images),
]

