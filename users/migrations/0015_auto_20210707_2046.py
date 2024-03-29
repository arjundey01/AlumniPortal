# Generated by Django 3.1.7 on 2021-07-07 20:46

import datetime
from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20210614_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='description',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='project',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='start_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='project',
            name='team',
            field=models.ManyToManyField(related_name='shared_project', to='users.Account'),
        ),
        migrations.AlterField(
            model_name='account',
            name='profile_img',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.profile_image_path),
        ),
        migrations.AlterField(
            model_name='pastjobs',
            name='description',
            field=models.CharField(default='', max_length=255),
        ),
    ]
