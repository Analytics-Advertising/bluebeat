# Generated by Django 5.0.6 on 2024-07-08 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealer', '0004_alter_application_date_applied'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Pre-Approved', 'Pre-Approved'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending', max_length=20),
        ),
    ]
