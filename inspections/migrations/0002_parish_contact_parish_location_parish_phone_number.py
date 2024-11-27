# Generated by Django 5.1.1 on 2024-11-26 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspections', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parish',
            name='contact',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='parish',
            name='location',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='parish',
            name='phone_number',
            field=models.CharField(default='', max_length=20),
        ),
    ]
