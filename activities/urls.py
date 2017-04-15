from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<activity_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^new/$', views.new, name='new'),
    url(r'^create/$', views.create, name='create'),
    url(r'^add_bookmark/$', views.create_bookmark, name='add_bookmark'),
    url(r'^delete_bookmark/$', views.delete_bookmark, name='add_bookmark'),
    url(r'^parse/$', views.parse, name='parse'),
    url(r'^refresh/$', views.refresh, name='refresh'),
    url(r'^change_status/$', views.change_status, name='change_status'),
]
