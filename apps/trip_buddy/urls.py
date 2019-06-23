from django.conf.urls import url 
from . import views

urlpatterns = [
  url(r'^$', views.index),
  url(r'^register$', views.register),
  url(r'^dashboard$', views.dashboard),
  url(r'^logout$', views.logout),
  url(r'^login$', views.login),
  url(r'^trips/new',views.trip_new),
  url(r'^trips/create', views.trip_create),
  url(r'^trips/edit/(?P<id>\d+)$',views.trip_edit),
  url(r'^trips/(?P<id>\d+)/make_edit$',views.make_edit),
  url(r'^trips/(?P<id>\d+)$',views.view_trip),
  url(r'^remove/(?P<id>\d+)$',views.remove_trip),
  url(r'^join/(?P<id>\d+)$', views.join_trip),
  url(r'^delete/(?P<id>\d+)$', views.delete_trip)
]