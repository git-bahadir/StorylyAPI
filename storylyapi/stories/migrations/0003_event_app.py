# Generated by Django 4.0.4 on 2022-04-24 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0002_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='app',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='event', to='stories.app'),
            preserve_default=False,
        ),
    ]