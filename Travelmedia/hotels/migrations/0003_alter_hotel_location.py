# Generated by Django 4.2.11 on 2024-03-31 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0002_hotelphoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='location',
            field=models.CharField(choices=[('Europe', 'Europe'), ('Western Europe', 'Western Europe'), ('Balkans', 'Balkans'), ('Eastern Europe', 'Eastern Europe')], max_length=30),
        ),
    ]
