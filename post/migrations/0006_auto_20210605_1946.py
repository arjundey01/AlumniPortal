# Generated by Django 3.1.7 on 2021-06-05 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20210605_1926'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='content',
            new_name='content_old',
        ),
    ]
