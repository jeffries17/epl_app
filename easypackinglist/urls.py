from django.urls import path, include
from . import views
from .views import about, user_trips_view

urlpatterns = [
    path('', views.home, name='home'),
    path('packing-list/', views.packing_list, name='packing_list'),
    path('packing-list/<uuid:trip_uuid>/', views.packing_list, name='packing_list_edit'),
    path('my-trips/', user_trips_view, name='my_trips'),
    path('delete-trip/<uuid:trip_uuid>/', views.delete_trip, name='delete_trip'),
    path('about/', about, name='about'),
    path('blog/', about, name='blog'),
]

# Add Django site authentication urls (for login, logout, password management)

