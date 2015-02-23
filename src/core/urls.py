from django.conf.urls import patterns, include, url

from . import views

urlpatterns = [
    url(r'^(?P<code>[\w-]+)/$', views.GroupScheduleView.as_view(), name='group'),
]
