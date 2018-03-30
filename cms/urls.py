from django.urls import path
from django.views.generic import TemplateView

from cms.views import PlaceCreateView


app_name = 'cms'

urlpatterns = [
    path('', TemplateView.as_view(template_name='cms/place_list.html'), name='place_list'),
    path('places/new', PlaceCreateView.as_view(), name='place_create'),
    path('places/<int:pk>', TemplateView.as_view(template_name='cms/place_list.html'), name='place_detail'),
]
