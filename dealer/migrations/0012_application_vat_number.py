# Generated by Django 5.0.6 on 2024-09-10 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealer', '0011_auto_20240723_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='vat_number',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
    ]
