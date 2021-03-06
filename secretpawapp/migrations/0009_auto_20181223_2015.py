# Generated by Django 2.1.1 on 2018-12-23 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('secretpawapp', '0008_auto_20181223_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='picture',
            field=models.ImageField(null=True, upload_to='file/character'),
        ),
        migrations.AlterField(
            model_name='character',
            name='tag',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='secretpawapp.Tag'),
        ),
        migrations.AlterField(
            model_name='gift',
            name='picture',
            field=models.ImageField(upload_to='file/gift'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(null=True, upload_to='file/avatar'),
        ),
    ]
