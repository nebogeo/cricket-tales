from django.conf.urls import patterns, url

from crickets import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.CricketView.as_view(), name='cricket'),
    url(r'^movie/(?P<pk>\d+)/$', views.MovieView.as_view(), name='movie'),
    url(r'^spit/', views.spit, name='spit'),
)
