# Generated by Django 2.1.5 on 2019-03-19 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("coderedcms", "0009_auto_20190201_1546")]

    operations = [
        migrations.AlterField(
            model_name="generalsettings",
            name="from_email_address",
            field=models.CharField(
                blank=True,
                help_text='The default email address this site appears to send from. For example: "sender@example.com" or "Sender Name <sender@example.com>" (without quotes)',
                max_length=255,
                verbose_name="From email address",
            ),
        )
    ]
