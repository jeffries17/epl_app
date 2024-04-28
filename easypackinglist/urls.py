from django.urls import path, include
from . import views
# from .views import about, user_trips_view

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home, name='home2'),
    # path('packing-list/', views.packing_list, name='packing_list'),
    # # Path for editing an existing trip (includes UUID)
    # path('packing-list/<uuid:trip_uuid>/', views.packing_list, name='packing_list_edit'),
    # # viewing my trips
    # path('my-trips/', user_trips_view, name='my_trips'),
    # # deleting trips
    # path('delete-trip/<uuid:trip_uuid>/', views.delete_trip, name='delete_trip'),
    # path('about/', about, name='about'),
]
