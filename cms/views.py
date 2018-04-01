from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView

from cms.models import Place


class PlaceCreateView(CreateView):
    model = Place
    fields = ('picture', 'details', 'size', 'price')


class PlaceDetailView(DetailView):
    model = Place


class PlaceListView(ListView):
    model = Place
