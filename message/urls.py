from django.urls import path
from .views import get_location_info
urlpatterns = [
    path('get_country/', get_location_info, name='get_country'),
]