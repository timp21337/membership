from django.conf.urls import patterns, include, url
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'membership.views.home', name='home'),
    # url(r'^membership/', include('membership.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^(favicon\.ico)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^robots\.txt$', 'django.views.static.serve', {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    url(r'^$', 'membership.views.home'),
    url(r'^home$', 'membership.views.home'),
    url(r'^login$', 'membership.views.login'),
    url(r'^logout$', 'membership.views.logout'),
    url(r'^carers$', 'membership.views.carers'),
    url(r'^members$', 'membership.views.members'),
    url(r'^member$', 'membership.views.member'),
    url(r'^session$', 'membership.views.session'),

)
