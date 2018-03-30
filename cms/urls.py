from django.urls import path

from cms.views import PlaceCreateView, PlaceDetailView, PlaceListView


app_name = 'cms'

urlpatterns = [
    path('', PlaceListView.as_view(), name='place_list'),
    path('places/new', PlaceCreateView.as_view(), name='place_create'),
    path('places/<int:pk>', PlaceDetailView.as_view(), name='place_detail'),
]
