# Generated by Django 3.0.3 on 2022-04-07 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liveness', '0002_auto_20220407_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='confidence_age',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='result',
            name='prediction_age',
            field=models.IntegerField(),
        ),
    ]
