# Generated by Django 4.0.6 on 2022-08-04 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coderedcms', '0033_alter_coderedpage_struct_org_actions_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carousel',
            name='animation',
        ),
        migrations.RemoveField(
            model_name='layoutsettings',
            name='navbar_wrapper_fluid',
        ),
    ]
