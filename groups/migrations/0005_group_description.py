# Generated by Django 3.1.7 on 2021-05-22 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_auto_20210522_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
