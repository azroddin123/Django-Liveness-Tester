# Generated by Django 3.0.3 on 2022-04-12 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liveness', '0009_auto_20220412_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='thumbnail_img_name',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
