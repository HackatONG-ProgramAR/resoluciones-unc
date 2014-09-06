from django.conf.urls import patterns, url

from document import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<number>\d+)$', views.document, name='document'),

    url(r'^(?P<number>\d+)/offset/(?P<offset>\d+)$', views.offset, name='offset'),
    url(r'^(?P<number>\d+)/file/(?P<index>\d+)$', views.file, name='file'),
    url(r'^(?P<number>\d+)/occurrence/(?P<occurrence>\d+)$', views.occurrence, name='occurrence'),
    url(r'^person/(?P<id>\d+)$', views.person, name='person'),
    url(r'^date/(?P<id>\d+)$', views.date, name='date'),
    url(r'^document/(?P<id>\d+)$', views.document, name='document'),
)
