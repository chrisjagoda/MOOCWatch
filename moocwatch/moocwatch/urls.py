from datetime import datetime
from django.conf.urls import url, include
from django.contrib.auth.views import password_reset_confirm, login, logout
from django.views.generic import TemplateView
from rest_framework import routers, urls

import app.views

from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('django.contrib.auth.urls')),
    # Included for Email Url Template
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm, name='password_reset_confirm'),
    # REST API URLS
    url(r'^api/rest-auth/', include('rest_auth.urls')),
    url(r'^api/rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/courses/$', app.views.CourseViewSet.as_view({'get': 'list'})),
    url(r'^api/courses/(?P<pk>[0-9]+)/$', app.views.CourseViewSet.as_view({'get': 'retrieve'})),
    url(r'^api/rest-auth/coursetakers/$', app.views.CourseTakerViewSet.as_view({'get': 'list', 'post':'create'})),
    url(r'^api/rest-auth/coursetakers/(?P<pk>[0-9]+)/$', app.views.CourseTakerViewSet.as_view({'get': 'retrieve',
                                                                                 'put': 'update',
                                                                                 'patch': 'partial_update',
                                                                                 'delete': 'destroy'})),
    url(r'^account-confirm-email/(?P<key>\w+)/$', TemplateView.as_view(),
        name='account_confirm_email'),
]