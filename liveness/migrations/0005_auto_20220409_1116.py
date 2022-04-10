# Generated by Django 3.0.3 on 2022-04-09 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liveness', '0004_auto_20220408_0816'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='folder_name',
            new_name='folder_path',
        ),
        migrations.AddField(
            model_name='task',
            name='live_images',
            field=models.IntegerField(default=0, help_text='live image count'),
        ),
        migrations.AddField(
            model_name='task',
            name='live_percentage',
            field=models.FloatField(default=0, help_text='percenage count of live images'),
        ),
        migrations.AddField(
            model_name='task',
            name='skipped_images',
            field=models.IntegerField(default=0, help_text='akipped image  in given folder'),
        ),
        migrations.AddField(
            model_name='task',
            name='spoof_images',
            field=models.IntegerField(default=0, help_text='spoof images count here'),
        ),
        migrations.AlterField(
            model_name='task',
            name='total_images',
            field=models.IntegerField(default=0, help_text='count total images in given folder'),
        ),
    ]
