# Generated by Django 2.1.4 on 2018-12-23 17:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('firstname', models.CharField(default='', max_length=250)),
                ('lastname', models.CharField(default='', max_length=250)),
                ('image', models.CharField(default='', max_length=500)),
                ('birthday', models.CharField(default='', max_length=50)),
                ('gender', models.CharField(default='', max_length=50)),
                ('bio', models.TextField(default='')),
                ('followers', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
