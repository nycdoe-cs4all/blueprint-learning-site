from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_resources, name='list_resources'),
    url(r'^parse', views.import_google_doc, name='parse_google_doc'),
    url(r'^edit/(?P<pk>\d+)$', views.edit_resource, name='edit_resource'),
    url(r'^new$', views.create_resource, name='create_resource'),
    url(r'^(?P<pk>[0-9]+)/$', views.show_resource, name='show_resource'),
    url(r'^delete/(?P<pk>\d+)$', views.delete_resource, name='delete_resource'),
]

