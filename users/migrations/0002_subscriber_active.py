# Generated by Django 2.1.7 on 2019-02-27 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]