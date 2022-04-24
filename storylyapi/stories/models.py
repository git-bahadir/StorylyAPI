import datetime
from django.db import models


class App(models.Model):
    pass

class Story(models.Model):
    ts = models.DateTimeField(auto_now_add=True)
    app = models.ForeignKey(App, related_name='story', on_delete=models.CASCADE)

class Metadata(models.Model):
    metadata = models.TextField()
    story = models.ForeignKey(Story, related_name='metadata', on_delete=models.CASCADE)