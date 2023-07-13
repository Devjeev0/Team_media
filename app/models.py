from django.db import models
from django.utils import timezone
from datetime import time

# class Room(models.Model):
#     room_name = models.CharField(max_length=100)
#
#     def get_booked_slots(self, date):
#         return Team.objects.filter(room=self, time__date=date)
#
# class Timing(models.Model):
#     date = models.DateField()
#     time_from = models.TimeField()
#     time_to = models.TimeField()
#     room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='timings')
#
#     def __str__(self):
#         return f"{self.room.name} - {self.date} {self.time_from}-{self.time_to}"
#
# class Team(models.Model):
#     team_name = models.CharField(max_length=100, default='')
#     name = models.CharField(max_length=100, default='')
#     work = models.TextField(default='')
#     room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
#     time = models.ForeignKey(Timing, on_delete=models.CASCADE, related_name='team', default=None)
#
#     def __str__(self):
#         return self.team_name

class Room(models.Model):
    room_name = models.CharField(max_length=100)

    def get_booked_slots(self, date):
        return Team.objects.filter(room=self, time__date=date)

class Timing(models.Model):
    date = models.DateField()
    time_from = models.TimeField()
    time_to = models.TimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='timings')

    def __str__(self):
        return f"{self.room.name} - {self.date} {self.time_from}-{self.time_to}"

class Team(models.Model):
    team_name = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, default='')
    work = models.TextField(default='')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    time = models.ForeignKey(Timing, on_delete=models.CASCADE, related_name='Team', default=None)

    def __str__(self):
        return self.team_name


