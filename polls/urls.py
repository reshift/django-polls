from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^latest/?$','polls.views.latest', name='PollLatest'),
    url(r'^form/(?P<id>[0-9]+)/?$','polls.views.form', name='PollForm'),
    url(r'^vote/(?P<id>[0-9]+)/?$','polls.views.vote', name='PollVote'),
    url(r'^results/(?P<id>[0-9]+)/?$','polls.views.results', name='PollResults'),
)
