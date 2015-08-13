from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.flatpages import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^groups/?$',
        'main.views.groups',
        name='groups'),

    url(r'^students/?$',
        'main.views.students',
        name='students'),

    url(r'^auth/login/?$',
        'main.views.login',
        name='login'),

    url(r'^auth/logout/?$',
        'main.views.logout',
        name='logout'),

    url(r'^auth/register/?$',
        'main.views.register',
        name='register'),

)


# main page, also catching all other paths
urlpatterns += patterns('', url(r'^(?P<optional>(.*))/?$',
                                'main.views.list_view',
                                name='list_view'))
