# Generated by Django 2.1.1 on 2018-12-27 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretpawapp', '0016_characternsfwtypes_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gift',
            name='picture',
            field=models.ImageField(null=True, upload_to='gift'),
        ),
    ]
