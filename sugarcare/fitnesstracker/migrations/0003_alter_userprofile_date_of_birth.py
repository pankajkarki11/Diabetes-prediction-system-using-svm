# Generated by Django 5.1.4 on 2025-01-21 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitnesstracker', '0002_alter_userprofile_age_alter_userprofile_height_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
