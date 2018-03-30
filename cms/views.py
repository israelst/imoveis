from django.shortcuts import render
from django.views.generic import CreateView, DetailView

from cms.models import Place


class PlaceCreateView(CreateView):
    model = Place
    fields = ('details', 'size', 'price')


class PlaceDetailView(DetailView):
    model = Place
