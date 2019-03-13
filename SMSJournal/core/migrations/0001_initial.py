# Generated by Django 2.1.7 on 2019-02-27 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Metrics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(auto_now_add=True)),
                ('current', models.BooleanField(default=False)),
                ('total_active_users', models.IntegerField()),
                ('daily_active_users', models.IntegerField()),
                ('added_active_users', models.IntegerField()),
                ('journal_entries_sent', models.IntegerField()),
                ('main_page_visits', models.IntegerField()),
            ],
        ),
    ]