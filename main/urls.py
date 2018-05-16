# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from . import views
from blog import views as blog_view
from django.contrib.auth import views as auth_views
urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout', kwargs={'next_page': 'login'}),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^post_list/$', blog_view.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', blog_view.post_detail, name='post_detail'),
    url(r'^post/new/$', blog_view.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', blog_view.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/delete/$', blog_view.post_delete, name='post_delete'),
    url(r'^my_info/$', views.my_info, name='my_info'),
    url(r'^my_info/(?P<pk>\d+)/edit/$', views.my_info_edit, name='my_info_edit'),
    url(r'^product/$', views.product, name='product'),
]
