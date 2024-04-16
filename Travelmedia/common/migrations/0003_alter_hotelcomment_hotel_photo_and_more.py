# Generated by Django 4.2.11 on 2024-03-27 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0002_hotelphoto'),
        ('common', '0002_alter_hotelcomment_hotel_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelcomment',
            name='hotel_photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='comments', to='hotels.hotelphoto'),
        ),
        migrations.AlterField(
            model_name='hotellike',
            name='hotel_photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='likes', to='hotels.hotelphoto'),
        ),
    ]
