"""ProDjango URL Configuration

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
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.views import generic
from coltrane.models import Entry

entry_info_dict = {
    'date_field': 'pub_date',
    'queryset': Entry.objects.all(),
    'month_format': '%m',
}

urlpatterns = [
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.TINY_MCE_ROOT}),

    url(r'weblog/$', generic.ArchiveIndexView.as_view(queryset=Entry.objects.all(), date_field='pub_date')),
    url(r'weblog/(?P<year>\d{4})/(?P<month>\d{2})/$',
        generic.MonthArchiveView.as_view(**entry_info_dict)),
    url(r'weblog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        generic.DateDetailView.as_view(**entry_info_dict)),

    url(r'^search/$', 'search.views.search'),
    # url(r'', include('django.contrib.flatpages.urls')),



]
