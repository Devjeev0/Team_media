from django.contrib.sites import requests
from rest_framework import viewsets
from .models import *
from django.shortcuts import render
from .serializers import *


# class RoomViewSet(viewsets.ModelViewSet):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def list(self, request, *args, **kwargs):
        rooms = self.get_queryset()
        serializer = self.get_serializer(rooms, many=True)
        return render(request, 'table.html', {'rooms': serializer.data})
# from rest_framework.decorators import api_view
# from rest_framework import viewsets
# from rest_framework.response import Response
#
# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# def room_view(request):
#     if request.method == 'GET':
#         queryset = Room.objects.all()
#         serializer = RoomSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = RoomSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
#
# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def room_detail_view(request, pk):
#     try:
#         room = Room.objects.get(pk=pk)
#     except Room.DoesNotExist:
#         return Response(status=404)
#
#     if request.method == 'GET':
#         serializer = RoomSerializer(room)
#         return Response(serializer.data)
#     elif request.method == 'PUT' or request.method == 'PATCH':
#         serializer = RoomSerializer(room, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
#     elif request.method == 'DELETE':
#         room.delete()
#         return Response(status=204)


# views.py

# views.py

import requests
from django.shortcuts import render


def room_table_view(request):
    # Fetch the timings data from the API or database
    try:
        response = requests.get('http://localhost:8000/rooms/')
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            timings = data
        else:
            timings = data.get('timings', [])
    except (requests.RequestException, ValueError):
        timings = []

    context = {'timings': timings}
    return render(request, 'index.html', context)

