# Generated by Django 4.2.7 on 2023-11-19 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashbord', '0009_alter_recognizedalphabet_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='recognizedalphabet',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='pdfs/'),
        ),
    ]