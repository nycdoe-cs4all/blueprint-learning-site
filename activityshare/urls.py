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


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^units/', include('activities.urls')),
    url(r'^users/', include('activities.user_urls')),
    url(r'^resources/', include('activities.resource_urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/', MyRegistrationView.as_view(), name = 'registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^about/$', TemplateView.as_view(template_name='about.html')),
    url(r'^what-is-cs/$', TemplateView.as_view(template_name='what_is_cs.html')),
    url(r'^meaningful-cs/$', TemplateView.as_view(template_name='meaningful_cs.html')),
    url(r'^concepts/$', TemplateView.as_view(template_name='concepts.html')),
    url(r'^practices/$', TemplateView.as_view(template_name='practices.html')),
    url(r'^perspectives/$', TemplateView.as_view(template_name='perspectives.html')),
    url(r'^outcomes/$', TemplateView.as_view(template_name='outcomes.html')),
    url(r'^curriculum/$', TemplateView.as_view(template_name='curriculum.html')),
    url(r'^curriculum/computational-media-explorer/$', TemplateView.as_view(template_name='computational-media-explorer.html')),  
    url(r'^curriculum/computational-media-creator/$', TemplateView.as_view(template_name='computational-media-creator.html')),
    url(r'^curriculum/computational-media-innovator/$', TemplateView.as_view(template_name='computational-media-innovator.html')),
    url(r'^curriculum/intro-to-pcomp/$', TemplateView.as_view(template_name='intro-to-pcomp.html')),
    url(r'^curriculum/intro-to-computational-media/$', TemplateView.as_view(template_name='intro-to-computational-media.html')),
    url(r'^curriculum/cs-discoveries/$', TemplateView.as_view(template_name='cs-discoveries.html')),
    url(r'^curriculum/exploring-cs/$', TemplateView.as_view(template_name='exploring-cs.html')),
    url(r'^curriculum/teals-intro-to-cs/$', TemplateView.as_view(template_name='teals-intro-to-cs.html')),
    url(r'^curriculum/codeorg-cs-principles/$', TemplateView.as_view(template_name='codeorg-cs-principles.html')),
    url(r'^curriculum/uteach-cs-principles/$', TemplateView.as_view(template_name='uteach-cs-principles.html')),
    url(r'^curriculum/bjc-cs-principles/$', TemplateView.as_view(template_name='bjc-cs-principles.html')),
    url(r'^curriculum/software-engineering-program/$', TemplateView.as_view(template_name='software-engineering-program.html')),
    url(r'^curriculum/software-engineering-program-jr/$', TemplateView.as_view(template_name='software-engineering-program-jr.html')),
    
]
