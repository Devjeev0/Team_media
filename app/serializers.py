from rest_framework import serializers
from .models import Room, Team, Timing
from datetime import datetime, time, timedelta, date
from django.utils import timezone




# class TeamSerializer(serializers.ModelSerializer):
#     date = serializers.DateField(source='time.date', read_only=True)

#     class Meta:
#         model = Team
#         fields = '__all__'
class TeamSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source='time.date', read_only=True)
    time_from = serializers.TimeField(source='time.time_from', read_only=True)
    time_to = serializers.TimeField(source='time.time_to', read_only=True)

    class Meta:
        model = Team
        fields = ['team_name', 'date', 'time_from', 'time_to', 'room', 'work', 'time']

        

class TimingSerializer(serializers.ModelSerializer):
    bookings = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = Timing
        fields = ['date', 'time_from', 'time_to', 'room', 'bookings']

    def get_bookings(self, obj):
        team_instances = Team.objects.filter(time=obj)
        return TeamSerializer(team_instances, many=True).data


class RoomSerializer(serializers.ModelSerializer):
    timings = TimingSerializer(many=True, read_only=True)
    bookings = TeamSerializer(many=True, read_only=True)
    free_slots = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'room_name', 'timings', 'bookings', 'free_slots']

    def get_free_slots(self, obj):
        timings = obj.timings.all().order_by('date', 'time_from')
        free_slots = []

        min_date = timings.first().date if timings.exists() else timezone.now().date()
        max_date = timings.last().date if timings.exists() else timezone.now().date()

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

# class TeamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Team
#         fields = '__all__'

# class TimingSerializer(serializers.ModelSerializer):
#     bookings = TeamSerializer(many=True, read_only=True)

#     class Meta:
#         model = Timing
#         fields = ['id', 'date', 'time_from', 'time_to', 'room', 'bookings']

# class RoomSerializer(serializers.ModelSerializer):
#     timings = TimingSerializer(many=True, read_only=True)
#     bookings = TeamSerializer(many=True, read_only=True)
#     free_slots = serializers.SerializerMethodField()

#     class Meta:
#         model = Room
#         fields = ['id', 'room_name', 'timings', 'bookings', 'free_slots']

#     def get_free_slots(self, obj):
#         timings = obj.timings.all().order_by('date', 'time_from')
#         free_slots = []

#         min_date = timings.first().date if timings.exists() else timezone.now().date()
#         max_date = timings.last().date if timings.exists() else timezone.now().date()

#         current_date = min_date
#         while current_date <= max_date:
#             time_slots = self.get_time_slots(obj, current_date)
#             free_slots.extend(time_slots)
#             current_date += timedelta(days=1)

#         return free_slots

#     def get_time_slots(self, obj, date):
#         timings = obj.timings.filter(date=date).order_by('time_from')
#         time_slots = []

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
#                     })
#                 start_time = timing.time_to

#             end_time = time.max
#             if start_time != end_time:
#                 time_slots.append({
#                     'date': date,
#                     'start_time': start_time,
#                     'end_time': end_time,
#                 })

#         return time_slots

