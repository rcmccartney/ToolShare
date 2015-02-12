from django.conf.urls import patterns, include, url
from Sharing import views

urlpatterns = patterns('',
    #+++++++++++++++ URLS related to the SHED over here+++++++++++++++++++ #
    url(r'^sheds/$', views.sheds, name='sheds'),
    url(r'^sheds/create/$', views.shedcreate, name='shedcreate'),
    url(r'^sheds/(?P<shed_id>\d+)/$',views.sheddetail, name='sheddetail'),
    url(r'^sheds/(?P<shed_id>\d+)/edit/$', views.shededit, name='shededit'),
    url(r'sheds/(?P<shed_id>\d+)/coords/$', views.shedcoords, name='shedcoords'),
    url(r'sheds/(?P<shed_id>\d+)/coords/add/$',views.shedaddcoords,name='shedaddcoords'),
    url(r'sheds/tooltransfer/(?P<tool_id>\d+)/$',views.tooltransfer,name = 'tooltransfer'),
    #+++++++++++++++++SHED url ends here ++++++++++++++++++++++++++++++++++#
    url(r'^create-request/(?P<tool_id>\d+)/$', views.create_request, name='create-request'),
    url(r'^received-requests/$', views.received_requests_index, name='received-requests'),
    url(r'^asked-requests/$', views.asked_requests_index, name='asked-requests'),
    url(r'^received-requests/(?P<tool_request_id>\d+)/$', views.received_request_detail, name='received-request-detail'),
    url(r'^asked-requests/(?P<tool_request_id>\d+)/$', views.asked_request_detail, name='asked-request-detail'),
)
