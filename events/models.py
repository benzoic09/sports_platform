from django.db import models
from sports.models import Sport


class Event(models.Model):
    sport = models.ForeignKey(
        Sport,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    venue = models.CharField(max_length=200)

    event_date = models.DateField()

    event_time = models.TimeField()

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title