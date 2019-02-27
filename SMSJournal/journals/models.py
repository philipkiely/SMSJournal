from django.db import models
from django.contrib.auth.models import User
import hashlib


#Static Method
def process_journal_name(s):
    s = s.lower()
    h = hashlib.sha256()
    h.update(s.encode())
    return h.hexdigest()


# Create your models here.
class Journal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150) #treated as case insensitive and hashed, see above
    google_docs_id = models.CharField(max_length=150)

    def __str__(self):
        return self.user.username + " " + self.name
