from django.conf.urls import url

from . import views
# from .decorators import check_recaptcha

urlpatterns = [
    url(r'^(?P<user_id>[0-9]+)/$', views.user_details, name='user_detail'),
    url(r'^edit/$', views.edit_profile, name='edit_profile'),
]
