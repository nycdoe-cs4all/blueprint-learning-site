from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<user_id>[0-9]+)/$', views.user_details, name='user_detail'),
    url(r'^edit/$', views.edit_profile, name='edit_profile'),
]
