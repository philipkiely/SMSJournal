from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Journal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150) #treat as case insensitive, see clean()
    google_docs_id = models.CharField(max_length=150)

    def clean(self): #overwrite default clean
        cleaned_data = super(Journal, self).clean() #keep original clean
        cleaned_data["name"] = cleaned_data["name"].lower() #lowercase name
        return cleaned_data
