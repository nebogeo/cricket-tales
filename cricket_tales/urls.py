from django.conf.urls import patterns, include, url
from django.contrib import admin

import settings

admin.site.site_header = 'Wild Cricket Tales Admin'

urlpatterns = patterns('',
    url(r'^crickets/', include('crickets.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
