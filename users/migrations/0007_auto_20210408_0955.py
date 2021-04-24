# Generated by Django 3.1.7 on 2021-04-08 09:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0006_contact_education_experience_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='is_alumni',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='account',
            name='designation',
            field=models.ManyToManyField(related_name='employees', to='users.Designation'),
        ),
        migrations.AddField(
            model_name='account',
            name='organization',
            field=models.ManyToManyField(related_name='employees', to='users.Organization'),
        ),
    ]
