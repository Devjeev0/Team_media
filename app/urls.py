from django.urls import path, include
from rest_framework.routers import DefaultRouter


from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'data', View)  
router.register(r'rooms', RoomViewSet)
router.register(r'timings', TimingViewSet)
router.register(r'teams', TeamViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('room-bookings/', room_bookings, name='room_bookings'),
    # path('rooms/', room_view, name='room-list'),
    # path('rooms/<int:pk>/', room_detail_view, name='room-detail'),
    # path('room-table/', room_table_view, name='room_table'),
]


