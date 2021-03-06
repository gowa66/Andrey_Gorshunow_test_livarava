"""django_tlr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from notelist.views import NoteListView, AddNoteView, WidgetView, RandomNoteView
from request.views import (RequestListView, RequestCounterView, )

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', NoteListView.as_view(), name='home'),
    url(r'^add/$', AddNoteView.as_view(), name='add_note'),
    url(r'^widget/$', WidgetView.as_view(), name='widget'),
    url(r'^random/$', RandomNoteView.as_view(), name='random_note'),
    url(r'^request/$', RequestListView.as_view(), name='request'),
    url(r'^request-counter/$', RequestCounterView.as_view(), name='request-counter'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
