# Generated by Django 2.1.5 on 2019-01-14 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("coderedcms", "0006_mailchimpapisettings")]

    operations = [
        migrations.AlterModelOptions(
            name="googleapisettings", options={"verbose_name": "Google API"}
        ),
        migrations.AlterModelOptions(
            name="mailchimpapisettings", options={"verbose_name": "Mailchimp API"}
        ),
    ]
