from django.conf.urls import patterns, include, url

from .views import pages

urlpatterns = [
    url(r'^lessons/group/$', pages.GroupLessonsView.as_view(), name='group-lessons'),
    url(r'^lessons/course/$', pages.CourseLessonsView.as_view(), name='course-lessons'),
    url(r'^lessons/teacher/$', pages.TeacherLessonsView.as_view(), name='teacher-lessons'),
    url(r'^', pages.ScheduleAppView.as_view(), name='main'),
]
