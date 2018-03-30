from django.urls import path

from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='cms/place_list.html'), name='place_list'),
]
