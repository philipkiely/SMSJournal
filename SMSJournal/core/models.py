from django.db import models
from django.core.mail import EmailMessage


# Static Methods
def daily_metrics():
    yesterday = Metrics.objects.get(current=True)
    #yesterday.total_active_users = users_who_are_paying
    #yesterday.daily_active_users = users_who_have_sent_journal_entries
    #yesterday.added_active_users = paying_users_who_just_signed_up
    yesterday.current = False
    yesterday.save()
    today = Metrics(current=True,
                    total_active_users=0,
                    daily_active_users=0,
                    added_active_users=0,
                    journal_entries_sent=0,
                    main_page_visits=0)
    today.save()
    message = "Yesterday on SMSJournal:\n\n{} total active users, including {} daily active users and {} new activated users.\n\nThere were {} journal entries sent and {} visits to the main page.\n\nBecause you got this email, at least something on the server is working.".format(
        yesterday.total_active_users,
        yesterday.daily_active_users,
        yesterday.added_active_users,
        yesterday.journal_entries_sent,
        yesterday.main_page_visits
    )
    email = EmailMessage(to=["info@grammiegram.com"],
                         from_email="smsjournalanalytics@grammiegram.com",
                         reply_to=["info@grammiegram.com"],
                         subject="Daily SMSJournal Metrics",
                         body=message)
    email.send()


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
