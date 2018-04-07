from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView

from cms.forms import PlaceForm
from cms.models import Place


class PlaceCreateView(CreateView):
    model = Place
    form_class = PlaceForm


class PlaceDetailView(DetailView):
    model = Place


#class PlaceListView(ListView, FormMixin):
class PlaceListView(ListView):
    model = Place
    #form_class = myFormDaVidaAi

    #def form_valid(self, form):
    #    return url(com o point)
    #    return HttpResponseRedirect(self.get_success_url())

    def get_queryset(self):
        qs = super().get_queryset()
        GET = self.request.GET
        lat, lng = GET.get('lat'), GET.get('lng')
        if lat and lng:
            point = Point(float(lat), float(lng), srid=32140)
            distance = Distance('location', point)
            return qs.annotate(distance=distance).order_by('distance')
        return qs
