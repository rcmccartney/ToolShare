from toolapp import views
from django.conf.urls import patterns, include, url
from django.contrib import admin
from toolapp.forms import CustomRegistrationForm
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^accounts/register/$', views.UserRegistrationView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^index/', views.index, name='index'),
    url(r'^tools/register/$', views.tools_register, name='tools_register'),
    url(r'^tools/(?P<tool_id>[0-9]*)/borrow$', views.tools_borrow),
    url(r'^tools/(?P<tool_id>[0-9]*)/blackout_dates$', views.tools_blackout_dates, name="tools_blackout_dates"),
    url(r'^tools/(?P<tool_id>[0-9]*)/edit$', views.tools_edit, name="tools_edit"),
    url(r'^tools/register_completed/$', views.tools_register_completed, name='tools_register_completed'),
    url(r'^tools/borrow-completed/$', views.tools_borrow_completed, name='tools_borrow_completed'),
    url(r'^tools/(?P<tool_id>[0-9]*)/availability$', views.tools_availability),

    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^tools/$', views.tools, name='tools'),
    url(r'^my-tools/$', views.my_tools, name='my_tools'),
    url(r'^users/', views.index, name='index'),
    url(r'^borrow-requests/$', views.borrow_requests),
    # the 'name' value as called by the {% url %} template tag
    url(r'^(?P<user_id>\d+)/$', views.detail, name='detail'),
    url(r'^$', 'toolapp.views.home', name='home'),
    url(r'^profile/$', views.profile_view.as_view(), name='profile'),
    url(r'^messages/', include('postman.urls')),
    url(r'^community-shed/create/$', 'toolapp.views.community_shed_create'),
    url(r'^community-shed/created/$', 'toolapp.views.community_shed_created'),
    url(r'^community-shed/mylist/$', 'toolapp.views.community_shed_mylist', name="community_shed_mylist"),
    url(r'^tools/(?P<community_shed_id>[0-9]*)/community-shed$', views.tools_community_shed, name="tools_community_shed"),
    url(r'^stats/$', views.stats),
    url(r'^my-reservations/$', views.my_reservations),


    url(r'^borrow-requests/approve$', views.borrow_request_approve),
    url(r'^borrow-requests/reject$', views.borrow_request_reject),
    url(r'^borrow-requests/finish$', views.borrow_request_finish),

    url(r'^profile_personalInfo/$', 'toolapp.views.profile_personalInfo', name='profile_personalInfo'),
    url(r'^profile_preferences/$', 'toolapp.views.profile_preferences', name='profile_preferences'),
     # Password URL workarounds for Django 1.6:
    #   http://stackoverflow.com/questions/19985103/
    url(r'^password/change/$',
                    auth_views.password_change,
                    name='password_change'),
    url(r'^password/change/done/$',
                    auth_views.password_change_done,
                    name='password_change_done'),
    url(r'^password/reset/$',
                    auth_views.password_reset,
                    name='password_reset'),
    url(r'^accounts/password/reset/done/$',
                    auth_views.password_reset_done,
                    name='password_reset_done'),
    url(r'^password/reset/complete/$',
                    auth_views.password_reset_complete,
                    name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                    auth_views.password_reset_confirm,
                    name='password_reset_confirm'),

)
