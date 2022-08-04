from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Event(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    eventdate = models.DateTimeField(null=True, blank=True)
        
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["eventdate"]

    def __str__(self):
        return self.name + " - " + str(self.eventdate)