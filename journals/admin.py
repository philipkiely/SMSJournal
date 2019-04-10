from django.contrib import admin
from .models import Journal


# Register your models here.
class JournalAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Journal._meta.fields]


admin.site.register(Journal, JournalAdmin)
