from django.contrib.sites import requests
from rest_framework import viewsets
from .models import *
from django.shortcuts import render
from .serializers import *


# class RoomViewSet(viewsets.ModelViewSet):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer


from time import strptime

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def list(self, request, *args, **kwargs):
        rooms = self.get_queryset()
        serializer = self.get_serializer(rooms, many=True)

        for room_data in serializer.data:
            for free_slot in room_data['free_slots']:
                start_time_str = free_slot['start_time']
                end_time_str = free_slot['end_time']

                start_time_str = start_time_str.strftime("%H:%M:%S")
                end_time_str = end_time_str.strftime("%H:%M:%S")

                start_time = strptime(start_time_str, "%H:%M:%S")
                end_time = strptime(end_time_str, "%H:%M:%S")

                duration_seconds = (end_time.tm_hour * 3600 + end_time.tm_min * 60 + end_time.tm_sec) - (start_time.tm_hour * 3600 + start_time.tm_min * 60 + start_time.tm_sec)

                free_slot['duration'] = duration_seconds // 60

        return render(request, 'index.html', {'rooms': serializer.data})







