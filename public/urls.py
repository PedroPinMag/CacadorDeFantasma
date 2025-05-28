from django.urls import path
from . import views

app_name = 'public'

urlpatterns = [
    path('', views.fantasminha_tracker_page, name='fantasminha_tracker_page'), # Main page
    path('about/', views.about_page, name='about_page'),                     # About page
    path('contact/', views.contact_page, name='contact_page'),               # Contact page
    path('api/update-location/', views.api_update_location, name='api_update_location'),
    path('api/fantasminha-locations/', views.api_get_fantasminha_locations, name='api_get_fantasminha_locations'),
]