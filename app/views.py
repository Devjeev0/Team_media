from django.contrib.sites import requests
from rest_framework import viewsets
from .models import *
from django.shortcuts import render
from .serializers import *


# class RoomViewSet(viewsets.ModelViewSet):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer


from time import strptime


class View(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def list(self, request, *args, **kwargs):
        rooms = self.get_queryset()
        serializer = self.get_serializer(rooms, many=True)

        for room_data in serializer.data:
            #--------------------------------
            bookings_data = room_data['bookings']

            # Extract the required fields from each booking and store in a list of dictionaries
            bookings_list = []
            for booking_data in bookings_data:
                try:
                    booking_info = {
                        'team_name': booking_data['team_name'],
                        'date': booking_data['date'],
                        'time_from': booking_data['time_from'],
                        'time_to': booking_data['time_to'],
                    }
                except KeyError:
                    # Handle cases where 'time' key is not present
                    booking_info = {
                        'team_name': booking_data['team_name'],
                    }
                bookings_list.append(booking_info)

            # Replace the bookings data with the updated list of dictionaries
            room_data['bookings'] = bookings_list
            #--------------------------------
            for free_slot in room_data['free_slots']:
                start_time_str = free_slot['start_time'].strftime("%H:%M:%S")
                end_time_str = free_slot['end_time'].strftime("%H:%M:%S")

                start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
                end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()

                duration_seconds = (end_time.hour * 3600 + end_time.minute * 60 + end_time.second) - (start_time.hour * 3600 + start_time.minute * 60 + start_time.second)

                free_slot['duration'] = duration_seconds // 60

        return render(request, 'index.html', {'rooms': serializer.data})

#-------------------------------------------------->
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer 

class TimingViewSet(viewsets.ModelViewSet):
    queryset = Timing.objects.all()
    serializer_class = TimingSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
#<------------------------------------------------->

# from datetime import datetime, time, timedelta

# class RoomViewSet(viewsets.ModelViewSet):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer

#     def list(self, request, *args, **kwargs):
#         rooms = self.get_queryset()
#         serializer = self.get_serializer(rooms, many=True)

#         for room_data in serializer.data:
#             for timing in room_data['timings']:
#                 bookings = timing.get('teams', [])
#                 if not bookings:
#                     timing['teams'] = [{'team_name': 'No Team'}]
#                     timing['free_slots'] = [{
#                         'start_time': timing['time_from'],
#                         'end_time': timing['time_to'],
#                         'duration': self.get_duration_minutes(timing['time_from'], timing['time_to']),
#                     }]
#                 else:
#                     for booking in bookings:
#                         booking['free_slots'] = [{
#                             'start_time': timing['time_from'],
#                             'end_time': timing['time_to'],
#                             'duration': self.get_duration_minutes(timing['time_from'], timing['time_to']),
#                         }]

#         return render(request, 'table.html', {'rooms': serializer.data})

#     def get_duration_minutes(self, time_from, time_to):
#         time_from_dt = datetime.strptime(time_from, '%H:%M:%S').time()
#         time_to_dt = datetime.strptime(time_to, '%H:%M:%S').time()
#         duration = (datetime.combine(date.today(), time_to_dt) - datetime.combine(date.today(), time_from_dt)).total_seconds() // 60
#         return duration

