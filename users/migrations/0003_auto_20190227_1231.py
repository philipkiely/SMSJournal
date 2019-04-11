# Generated by Django 2.1.7 on 2019-02-27 12:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_subscriber_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='last_entry',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 27, 12, 31, 1, 141900, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='subscriber',
            name='total_entries',
            field=models.IntegerField(default=0),
        ),
    ]