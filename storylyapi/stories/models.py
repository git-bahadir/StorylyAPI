from django.db import models
from django.utils import timezone

class App(models.Model):
    pass

class Story(models.Model):
    ts = models.DateTimeField(default=None)
    app = models.ForeignKey(App, related_name='story', on_delete=models.CASCADE)

class Metadata(models.Model):
    metadata = models.TextField()
    story = models.ForeignKey(Story, related_name='metadata', on_delete=models.CASCADE)

class Event(models.Model):
    event_type = models.CharField(max_length=255)
    story = models.ForeignKey(Story, related_name='event', on_delete=models.CASCADE)
    app = models.ForeignKey(App, related_name='event', on_delete=models.CASCADE)
    count = models.IntegerField()
    date = models.DateField(default=timezone.now)