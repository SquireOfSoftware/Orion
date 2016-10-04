from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^missions', views.missions, name='missions'),
    url(r'^drones', views.drones, name='drones'),
    url(r'^media', views.media, name='media'),
]

