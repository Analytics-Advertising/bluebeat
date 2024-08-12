# Generated by Django 5.0.6 on 2024-07-08 07:23

from django.db import migrations

def add_user_roles(apps, schema_editor):
    #  create user roles
    UserRole = apps.get_model('system_management', 'UserType')
    user_roles = ['Admin', 
                  'Dealer'
                 ]
    [UserRole.objects.create(name=user_role) for user_role in user_roles]
       


class Migration(migrations.Migration):

    dependencies = [
        ('system_management', '0001_initial'),
    ]

    operations = [
         migrations.RunPython(add_user_roles),
    ]
