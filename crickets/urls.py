from django.conf.urls import patterns, url

from crickets import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^cricket/(?P<pk>\d+)/$', views.CricketView.as_view(), name='cricket'),
    url(r'^burrow/(?P<pk>\d+)/$', views.BurrowView.as_view(), name='burrow'),
    url(r'^movie/(?P<pk>\d+)/$', views.MovieView.as_view(), name='movie'),
    url(r'^player/(?P<pk>\d+)/$', views.PlayerView.as_view(), name='player'),
    url(r'^tutorial/', views.tutorial, name='tutorial'),
    url(r'^about/', views.about, name='about'),
    url(r'^suck/', views.suck, name='suck'),
    url(r'^spit_event/', views.spit_event, name='spit_event'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/$', views.logmein, name='login'),
    url(r'^logout/$', views.logmeout, name='logout'),
    url(r'^random_movie/$', views.random_movie, name='random_movie'),
)
