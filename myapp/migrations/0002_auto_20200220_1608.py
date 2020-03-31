# Generated by Django 3.0.3 on 2020-02-20 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio_info',
            name='Auto_Transcribed_Text',
            field=models.TextField(help_text='Auto Transcribed Text From The ASR'),
        ),
        migrations.AlterField(
            model_name='audio_info',
            name='wav_file_links',
            field=models.CharField(help_text='Audio Links', max_length=200),
        ),
    ]
