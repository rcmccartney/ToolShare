from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from djang.contrib import admin
from registration.backends.default.views import RegistrationView
#from toolapp.forms import CustomRegistrationForm

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'toolsite.views.home', name='home'),
    url(r'^accounts/register/$', 'registration.views.register',    {'form_class':CustomRegistrationForm}),
    url(r'^index/', include('toolapp.urls', namespace="toolapp")),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
)

