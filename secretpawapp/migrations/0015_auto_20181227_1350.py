# Generated by Django 2.1.1 on 2018-12-27 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretpawapp', '0014_auto_20181227_1308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='nsfw',
        ),
        migrations.AddField(
            model_name='character',
            name='nsfw',
            field=models.ManyToManyField(to='secretpawapp.CharacterNSFWTypes'),
        ),
    ]
