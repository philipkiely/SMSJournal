# Generated by Django 2.1.7 on 2019-04-01 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190315_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='verif_code',
            field=models.IntegerField(null=True),
        ),
    ]
