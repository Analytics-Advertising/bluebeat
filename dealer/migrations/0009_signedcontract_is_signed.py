# Generated by Django 5.0.6 on 2024-07-09 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealer', '0008_contractacknowledgement_signedcontract'),
    ]

    operations = [
        migrations.AddField(
            model_name='signedcontract',
            name='is_signed',
            field=models.BooleanField(default=False),
        ),
    ]
