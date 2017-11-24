"""activityshare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from activities.views import index as homepage, MyRegistrationView, edit_profile
from django.views.generic import TemplateView
# for captchas
# from django.contrib.auth import views as auth_views
# from activities.forms import CaptchaPasswordResetForm
# from django.contrib.auth.views import password_reset


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^units/', include('activities.urls')),
    url(r'^users/', include('activities.user_urls')),
    url(r'^resources/', include('activities.resource_urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/', MyRegistrationView.as_view(), name = 'registration_register'),
    # url(r'^accounts/password/reset/$',auth_views.password_reset, {'post_reset_redirect': '/accounts/password/reset/done/','password_reset_form': CaptchaPasswordResetForm},  name='password_reset'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^about/$', TemplateView.as_view(template_name='about.html')),
    url(r'^what-is-cs/$', TemplateView.as_view(template_name='what_is_cs.html')),
    url(r'^meaningful-cs/$', TemplateView.as_view(template_name='meaningful_cs.html')),
    url(r'^concepts/$', TemplateView.as_view(template_name='concepts.html')),
    url(r'^practices/$', TemplateView.as_view(template_name='practices.html')),
    url(r'^perspectives/$', TemplateView.as_view(template_name='perspectives.html')),
    url(r'^outcomes/$', TemplateView.as_view(template_name='outcomes.html')),
    url(r'^ican/$', TemplateView.as_view(template_name='ican.html')),

]
