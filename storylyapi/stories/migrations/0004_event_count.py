# Generated by Django 4.0.4 on 2022-04-25 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0003_event_app'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
