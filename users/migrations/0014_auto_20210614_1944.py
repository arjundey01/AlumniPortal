# Generated by Django 3.1.7 on 2021-06-14 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20210605_1410'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='designation',
        ),
        migrations.AddField(
            model_name='account',
            name='designation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='users.designation'),
        ),
        migrations.RemoveField(
            model_name='account',
            name='organization',
        ),
        migrations.AddField(
            model_name='account',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='users.organization'),
        ),
    ]
