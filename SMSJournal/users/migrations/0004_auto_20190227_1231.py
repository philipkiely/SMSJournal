# Generated by Django 2.1.7 on 2019-02-27 12:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190227_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='last_entry',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
