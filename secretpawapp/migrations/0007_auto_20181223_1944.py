# Generated by Django 2.1.1 on 2018-12-23 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretpawapp', '0006_auto_20181218_1500'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='profile',
        ),
        migrations.AddField(
            model_name='profile',
            name='characters',
            field=models.ManyToManyField(to='secretpawapp.Character'),
        ),
    ]
