# Generated by Django 5.2 on 2025-05-04 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feast', '0022_attendance_delete_inoutselection'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='expense',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
