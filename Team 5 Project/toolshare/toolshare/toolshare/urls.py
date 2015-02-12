from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import admin
from django.views.generic import RedirectView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='home/'), name='home'),
    url(r'^home/', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^about/', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('UserAuth.urls',namespace="users")),
    url(r'^toolmgmt/', include('ToolMgmt.urls', namespace="toolmgmt")),
    url(r'^sharing/', include('Sharing.urls', namespace="sharing")),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
)
