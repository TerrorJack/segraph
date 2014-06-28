from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/', login_view),
    url(r'^register/',register_view),
    url(r'^user/',user_view),
    url(r'^userprofile/',userprofile_view),
    url(r'^gal/',gal_view),
    url(r'^pic/',pic_view),
    url(r'^pic_new/',pic_new_view),
    url(r'^match/',match_view),
)
