from django.contrib import admin
from .models import Metrics


# Register your models here.
class MetricsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Metrics._meta.fields]


admin.site.register(Metrics, MetricsAdmin)
