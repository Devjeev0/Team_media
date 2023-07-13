from rest_framework import serializers
from .models import Room, Team, Timing
from datetime import datetime, time, timedelta
from django.utils import timezone

#
# class TeamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Team
#         fields = '__all__'
#         depth = 1
#
# class TimingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Timing
#         fields = '__all__'
#         depth = 1
#
# class RoomSerializer(serializers.ModelSerializer):
#     timings = TimingSerializer(many=True, read_only=True)
#     # bookings = TeamSerializer(many=True, read_only=True)
#     free_slots = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Room
#         fields = ['id', 'room_name', 'timings', 'free_slots']
#         depth = 1
#
#     def get_free_slots(self, obj):
#         timings = obj.timings.all().order_by('date', 'time_from')
#         free_slots = []
#
#         # Get the minimum and maximum dates from timings
#         min_date = timings.first().date if timings.exists() else timezone.now().date()
#         max_date = timings.last().date if timings.exists() else timezone.now().date()
#
#         # Iterate over each date
#         current_date = min_date
#         while current_date <= max_date:
#             time_slots = self.get_time_slots(obj, current_date)
#             free_slots.extend(time_slots)
#             current_date += timedelta(days=1)
#
#         return free_slots
#
#     def get_time_slots(self, obj, date):
#         timings = obj.timings.filter(date=date).order_by('time_from')
#         time_slots = []
#
#         if not timings.exists():
#             time_slots.append({
#                 'date': date,
#                 'start_time': time.min,
#                 'end_time': time.max,
#             })
#         else:
#             start_time = time.min
#             for timing in timings:
#                 if timing.time_from != start_time:
#                     time_slots.append({
#                         'date': date,
#                         'start_time': start_time,
#                         'end_time': timing.time_from,
#
#                     })
#                 start_time = timing.time_to
#
#             end_time = time.max
#             if start_time != end_time:
#                 time_slots.append({
#                     'date': date,
#                     'start_time': start_time,
#                     'end_time': end_time,
#                 })
#
#         return time_slots

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        depth = 1

class TimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timing
        fields = '__all__'
        depth = 1

class RoomSerializer(serializers.ModelSerializer):
    timings = TimingSerializer(many=True, read_only=True)
    bookings = TeamSerializer(many=True, read_only=True)  # Include the bookings field

    free_slots = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'room_name', 'timings', 'bookings', 'free_slots']  # Include the bookings field
        depth = 1

    def get_free_slots(self, obj):
        timings = obj.timings.all().order_by('date', 'time_from')
        free_slots = []

        # Get the minimum and maximum dates from timings
        min_date = timings.first().date if timings.exists() else timezone.now().date()
        max_date = timings.last().date if timings.exists() else timezone.now().date()

        # Iterate over each date
        current_date = min_date
        while current_date <= max_date:
            time_slots = self.get_time_slots(obj, current_date)
            free_slots.extend(time_slots)
            current_date += timedelta(days=1)

        return free_slots

    def get_time_slots(self, obj, date):
        timings = obj.timings.filter(date=date).order_by('time_from')
        time_slots = []

        if not timings.exists():
            time_slots.append({
                'date': date,
                'start_time': time.min,
                'end_time': time.max,
            })
        else:
            start_time = time.min
            for timing in timings:
                if timing.time_from != start_time:
                    time_slots.append({
                        'date': date,
                        'start_time': start_time,
                        'end_time': timing.time_from,
                    })
                start_time = timing.time_to

            end_time = time.max
            if start_time != end_time:
                time_slots.append({
                    'date': date,
                    'start_time': start_time,
                    'end_time': end_time,
                })

        return time_slots