# Generated by Django 5.2 on 2025-04-09 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feast', '0006_remove_profile_user_delete_loginattempt_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='menu_item',
        ),
        migrations.RemoveField(
            model_name='order',
            name='student',
        ),
        migrations.DeleteModel(
            name='Menu',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
