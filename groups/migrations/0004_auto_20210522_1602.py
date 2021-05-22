# Generated by Django 3.1.7 on 2021-05-22 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210517_1622'),
        ('groups', '0003_group_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='groups', to='users.Account'),
        ),
    ]
