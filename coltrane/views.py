from django.shortcuts import render_to_response
from models import Entry

# Create your views here.
def entries_index(request):
    return render_to_response('coltrane/entry_index.html',
                              {'entry_list': Entry.objects.all()})
