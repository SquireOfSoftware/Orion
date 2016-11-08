from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^missions/?$', views.handle_missions),
    url(r'^missions/(?P<mission_id>[0-9]{1,10})/?$', views.get_mission),
    url(r'^missions/(?P<mission_id>[0-9]{1,10})/start?$', views.start_mission),
    url(r'^missions/(?P<mission_id>[0-9]{1,10})/waypoints?$', views.get_mission_waypoints),
    url(r'^missions/(?P<mission_id>[0-9]{1,10})/status?$', views.get_mission_status),
    url(r'^missions/(?P<mission_id>[0-9]{1,10})/images?$', views.get_mission_images),
    url(r'^missions/(?P<mission_id>[0-9]{1,10})/images/date/?$', views.get_next_set_of_mission_images),
    url(r'^missions/(?P<mission_id>[0-9]{1,10})/images/id/(?P<image_id>[0-9]{1,5})?$',
        views.get_next_set_of_mission_images_via_image_id),
    url(r'^drones/?$', views.handle_drones),
    url(r'^drones/(?P<drone_id>[0-9]{1,10})/?$', views.get_drone),
    url(r'^drones/(?P<drone_id>[0-9]{1,10})/status?$', views.get_drone_status),
    url(r'^drones/(?P<drone_id>[0-9]{1,10})/metadata/current?$', views.get_drone_current_metadata),
    url(r'^drones/(?P<drone_id>[0-9]{1,10})/control/?$', views.control_drone),
    url(r'^images/?$', views.get_images),
    url(r'^images/(?P<image_id>[0-9]{1,10})/?$', views.get_image),
    url(r'^images/(?P<image_id>[0-9]{1,10})/filter?$', views.get_next_image_set),
    url(r'^images/current/?$', views.get_current_image),
    url(r'^images/missions/?$', views.get_mission_images),
    url(r'^missions/(?P<mission_id>[0-9]{1,10})/post/?$', views.post_test_image),
]

