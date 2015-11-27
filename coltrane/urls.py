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
from .models import Category,Entry, Link
from .views import category_detail

entry_info_dict = {
    'date_field': 'pub_date',
    'queryset': Entry.objects.all(),
    'month_format': '%m',
}

link_info_dict = {
    'date_field': 'pub_date',
    'queryset': Link.objects.all(),
    'month_format': '%m',
}

urlpatterns = [

    # For Categories
    url(r'categories/$', generic.ListView.as_view(
        queryset=Category.objects.all(),
        allow_empty=True,
    )),

    url(r'categories/(?P<slug>[-_\w]+)/$', category_detail, name='coltrane_category_detail'),

    # For entry
    url(r'^$', generic.ArchiveIndexView.as_view(
        queryset=Entry.objects.all(),
        date_field='pub_date',
        allow_empty=True)),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        generic.MonthArchiveView.as_view(**entry_info_dict)),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        generic.DateDetailView.as_view(**entry_info_dict), name='coltrane_entry_detail'),

    # For links
    url(r'^links/$', generic.ArchiveIndexView.as_view(queryset=Link.objects.all(), date_field='pub_date', allow_empty=True)),
    url(r'^links/(?P<year>\d{4})/(?P<month>\d{2})/$',
        generic.MonthArchiveView.as_view(**link_info_dict)),
    url(r'^links/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        generic.DateDetailView.as_view(**link_info_dict), name='coltrane_link_detail'),
]
