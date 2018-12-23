# Generated by Django 2.1.1 on 2018-12-23 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretpawapp', '0011_auto_20181223_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='picture',
            field=models.ImageField(null=True, upload_to='character'),
        ),
        migrations.AlterField(
            model_name='gift',
            name='picture',
            field=models.ImageField(upload_to='gift'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(null=True, upload_to='avatar'),
        ),
    ]
