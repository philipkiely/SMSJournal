from django.contrib import admin
from .models import Subscriber

# Register your models here.


class SubscriberAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Subscriber._meta.fields]


admin.site.register(Subscriber, SubscriberAdmin)
