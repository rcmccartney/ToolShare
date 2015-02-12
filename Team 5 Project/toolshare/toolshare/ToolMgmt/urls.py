from django.conf.urls import patterns, include, url
from ToolMgmt import views
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='tools/', permanent=False), name='tools'),
    url(r'^tools/$', views.index, name='tools'),
    url(r'^tools/mytools/', views.mytools, name='mytools'),
    url(r'^tools/register/$', views.register, name="register"),
    url(r'^tools/(?P<tool_id>\d+)/$', views.detail, name='detail'),
    url(r'^tools/(?P<tool_id>\d+)/edit/$', views.tool_edit, name='tool_editition'),
)
