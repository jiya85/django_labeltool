# Generated by Django 3.0.3 on 2020-03-30 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_auto_20200329_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='transindiv',
            name='counter_left',
            field=models.IntegerField(null=True),
        ),
    ]
