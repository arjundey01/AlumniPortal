# Generated by Django 3.1.2 on 2020-12-18 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('content', models.JSONField(default=dict)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='users.account')),
                ('likes', models.ManyToManyField(related_name='liked_posts', to='users.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='users.account')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='post.post')),
            ],
        ),
    ]
