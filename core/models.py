from django.db import models
from django.core.mail import EmailMessage
from users.models import Subscriber
import datetime
#TODO: round down to midnight on both new and cutoff, Delorean??


# Static Methods
def init_daily_metrics():
    today = Metrics(current=True,
                    total_active_users=0,
                    daily_active_users=0,
                    added_active_users=0,
                    journal_entries_sent=0,
                    main_page_visits=0)
    today.save()


def send_metrics(message, cutoff):
    email = EmailMessage(to=["info@grammiegram.com"],
                         from_email="smsjournalanalytics@grammiegram.com",
                         reply_to=["info@grammiegram.com"],
                         subject="Daily SMSJournal Metrics " + str(cutoff.month) + "/" + str(cutoff.day) + "/" + str(cutoff.year),
                         body=message)
    email.send()


def daily_metrics():
    try:
        yesterday = Metrics.objects.get(current=True) #update daily metrics for previous day
        yesterday.total_active_users = Subscriber.objects.filter(active=True).count()
        cutoff = datetime.datetime.now() - datetime.timedelta(days=1)
        yesterday.daily_active_users = Subscriber.objects.filter(active=True).filter(last_entry__gte=cutoff).count()
        yesterday.added_active_users = Subscriber.objects.filter(active=True).filter(user__date_joined__gte=cutoff).count()
        yesterday.current = False
        yesterday.save()
        message = "Yesterday on SMSJournal:\n\n{} total active users, including {} daily active users and {} new activated users.\n\nThere were {} journal entries sent and {} visits to the main page.\n\nBecause you got this email, at least something on the server is working.".format(
            yesterday.total_active_users,
            yesterday.daily_active_users,
            yesterday.added_active_users,
            yesterday.journal_entries_sent,
            yesterday.main_page_visits
        )
        send_metrics(message, cutoff)
    except:
        pass
    init_daily_metrics()


class Metrics(models.Model):
    day = models.DateField(auto_now_add=True)
    current = models.BooleanField(default=False)
    total_active_users = models.IntegerField()
    daily_active_users = models.IntegerField()
    added_active_users = models.IntegerField()
    journal_entries_sent = models.IntegerField()
    main_page_visits = models.IntegerField()

    def log_main_page_visit(self):
        self.main_page_visits += 1
        self.save()

    def log_journal_entry(self):
        self.journal_entries_sent += 1
        self.save()

    def __str__(self):
        return str(self.day.month) + "/" + str(self.day.day) + "/" + str(self.day.year)
