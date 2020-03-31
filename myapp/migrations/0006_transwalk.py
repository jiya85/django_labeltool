# Generated by Django 3.0.3 on 2020-03-11 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20200302_1316'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransWalk',
            fields=[
                ('ASRid', models.AutoField(primary_key=True, serialize=False)),
                ('Audio_File_Link', models.CharField(help_text='Audio Links', max_length=200)),
                ('Transcripted_Text', models.TextField(help_text='Most Recent Transcripted Text')),
                ('IsOpenFlag', models.BooleanField(default=False)),
                ('Updated_At', models.DateTimeField(auto_now_add=True)),
                ('Trans_Counter', models.IntegerField(default=0)),
                ('Transcribers_Checked', models.CharField(help_text='Usernames of the transcribers Who checked the specific audio', max_length=200)),
            ],
        ),
    ]
