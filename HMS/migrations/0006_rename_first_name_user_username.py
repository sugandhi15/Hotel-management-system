# Generated by Django 5.1.1 on 2024-11-01 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HMS', '0005_rename_customer_booking_user_alter_booking_room'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='first_name',
            new_name='username',
        ),
    ]