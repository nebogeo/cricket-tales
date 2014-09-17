from django.conf.urls import patterns, url

from crickets import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^cricket/(?P<pk>\d+)/$', views.CricketView.as_view(), name='cricket'),
    url(r'^movie/(?P<pk>\d+)/$', views.MovieView.as_view(), name='movie'),
    url(r'^suck/', views.suck, name='suck'),
    url(r'^spit_event/', views.spit_event, name='spit_event'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/$', views.logmein, name='login'),
    url(r'^logout/$', views.logmeout, name='logout'),
)
