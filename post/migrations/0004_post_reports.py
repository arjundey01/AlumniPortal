# Generated by Django 3.1.7 on 2022-01-15 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_merge_20211019_1452'),
        ('post', '0003_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reports',
            field=models.ManyToManyField(blank=True, related_name='reported_posts', to='users.Account'),
        ),
    ]
