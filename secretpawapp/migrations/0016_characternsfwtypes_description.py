# Generated by Django 2.1.1 on 2018-12-27 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretpawapp', '0015_auto_20181227_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='characternsfwtypes',
            name='description',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]
