from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.views import generic
from django_filters.views import object_filter

from models import Category, Entry


# Create your views here.
def entries_index(request):
    return render_to_response('coltrane/entry_archive.html',
                              {'entry_list': Entry.objects.all()})


def entry_detail(request, year, month, day, slug):
    import datetime
    import time
    date_stamp = time.strptime(year + month + day, "%Y%m%d")
    pub_data = datetime.date(*date_stamp[:3])

    entry = get_object_or_404(Entry,
                              pub_date__year=pub_data.year,
                              pub_date__month=pub_data.month,
                              pub_date__day=pub_data.day,
                              slug=slug)

    return render_to_response('coltrane/entry_detail.html',
                              {'entry': entry})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)

    return object_filter(request,
                         model=Entry,
                         template_name='coltrane/category_detail.html',
                         queryset=category.entry_set.all(),
                         extra_context={'category': category})
