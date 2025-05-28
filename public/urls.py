# public/urls.py
from django.urls import path
from . import views

app_name = 'public'

urlpatterns = [
    # ... other urls ...
    path('api/update-location/', views.api_update_location, name='api_update_location'),
    path('api/fantasminha-locations/', views.api_get_fantasminha_locations, name='api_get_fantasminha_locations'),
    path('', views.fantasminha_tracker_page, name='fantasminha_tracker_page'), # Main page
]