# Generated by Django 4.2.7 on 2023-11-15 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashbord', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recognizedalphabet',
            name='timestamp',
        ),
    ]