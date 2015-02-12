from django.conf.urls import patterns,url
from UserAuth import views

urlpatterns = patterns('' ,
        url(r'^signup/$', views.sign_up, name='sign_up'),
        url(r'^login/$',views.user_login, name='login'),
        url(r'^$',views.user_login, name='login'),
        url(r'^edit/$',views.user_edit, name='edit'),
        url(r'^logout/$',views.user_logout, name='logout'),
        url(r'^preferences/$',views.user_preferences, name = 'preferences'), 
        url(r'^changepassword/$',views.changepassword, name = 'change_password'),
        )
