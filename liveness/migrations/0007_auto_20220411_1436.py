# Generated by Django 3.0.3 on 2022-04-11 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liveness', '0006_result_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
