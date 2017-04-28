from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main$', views.main, name="mainpage"),
    url(r'^process/(?P<userid>\d+)$', views.process, name="process"),
    url(r'^edit/(?P<apptid>\d+)$', views.edit, name="edit"),
    url(r'^update/(?P<apptid>\d+)$', views.update, name="update"),
    url(r'^delete/(?P<apptid>\d+)$', views.delete, name="delete"),
]
