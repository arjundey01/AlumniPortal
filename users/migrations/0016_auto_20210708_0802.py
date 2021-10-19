# Generated by Django 3.1.7 on 2021-07-08 08:02

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20210707_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='education',
            name='description',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='education',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='education',
            name='start_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='experience',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='users.organization'),
        ),
    ]