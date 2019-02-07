from django.db import models


# Create your models here.
class Journal(models.Model):
    name = models.CharField(max_length=100) #treat as case insensitive, see clean()
    google_docs_id = models.CharField(max_length=100)
    phone_number = models.BigIntegerField()
    #user = models.ForeignKey()

    def clean(self): #overwrite default clean
        cleaned_data = super(Journal, self).clean() #keep original clean
        cleaned_data["name"] = cleaned_data["name"].lower() #lowercase name
        return cleaned_data
