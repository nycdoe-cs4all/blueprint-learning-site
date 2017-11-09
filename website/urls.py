from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^accounts/password/reset/$', views.edit_profile, name='edit_profile')
]
