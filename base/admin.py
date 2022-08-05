from django.contrib import admin
from .models import Event, Topic, Messages
# Register your models here.
admin.site.register(Event)
admin.site.register(Topic)
admin.site.register(Messages)