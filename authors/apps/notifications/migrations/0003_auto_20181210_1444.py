# Generated by Django 2.1.3 on 2018-12-10 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20181205_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.AlterField(
            model_name='notification',
            name='article',
            field=models.ManyToManyField(to='articles.Article'),
        ),
        migrations.DeleteModel(
            name='Article',
        ),
    ]
