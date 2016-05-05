from django.conf.urls import patterns, url
from django.conf.urls import include

from crickets import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^movie/(?P<pk>\d+)/$', views.MovieView.as_view(), name='movie'),
    url(r'^meadow/$', views.meadow, name='meadow'),
    url(r'^house/(?P<burrow_id>\d+)/(?P<house>\w+)/$', views.house, name='house'),
    url(r'^tutorial/', views.tutorial, name='tutorial'),
    url(r'^tutorial-basic', views.tutorial_basic, name='tutorial_basic'),
    url(r'^tutorial-movement', views.tutorial_movement, name='tutorial_movement'),
    url(r'^tutorial-predators', views.tutorial_predators, name='tutorial_predators'),
    url(r'^tutorial-id', views.tutorial_id, name='tutorial_id'),
    url(r'^tutorial-ready', views.tutorial_ready, name='tutorial_ready'),
    url(r'^faq/', views.faq, name='faq'),
    url(r'^about/', views.about, name='about'),
#    url(r'^suck/', views.suck, name='suck'),
    url(r'^spit_event/', views.spit_event, name='spit_event'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/$', views.logmein, name='login'),
    url(r'^logout/$', views.logmeout, name='logout'),
    url(r'^random_movie/$', views.random_movie, name='random_movie'),
    url(r'^house_builder/(?P<id>\d+)/$', views.house_builder, name='house_builder'),
    url(r'^random_burrow_movie/(?P<id>\d+)/$', views.random_burrow_movie, name='random_burrow_movie'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^get-data/', views.get_data, name='get-data'),
)
