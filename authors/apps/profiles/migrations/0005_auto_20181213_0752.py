# Generated by Django 2.1.2 on 2018-12-13 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20181213_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(default='my auto bio'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.CharField(default='', max_length=255),
        ),
    ]
