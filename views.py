from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from ownYourLife.models import Category, Entry

class IndexView(generic.ListView):
    model = Entry
    template_name = 'ownYourLife/index.html'
    context_object_name = 'model'

    def get_queryset(self):
        """Return the last five recorded entries."""
        return Entry.objects.all() #order_by('-timestamp')[:5]

class AddView(generic.DetailView):
    model = Entry
    template_name = 'ownYourLife/add.html'

class EntryDetailView(generic.DetailView):
    model = Entry
    template_name = 'ownYourLife/detail.html'
