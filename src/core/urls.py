from django.conf.urls import patterns, include, url

from . import views

urlpatterns = [
    url(r'^lessons/$', views.LessonsView.as_view(), name='lessons'),
    url(r'^', views.ScheduleAppView.as_view(), name='main'),
]
