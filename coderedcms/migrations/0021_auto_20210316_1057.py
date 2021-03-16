# Generated by Django 3.1.7 on 2021-03-16 14:57

from django.db import migrations


def add_navbar_orderables(apps, schema_editor):
    Navbar = apps.get_model('coderedcms', 'Navbar')
    NavbarOrderable = apps.get_model('coderedcms', 'NavbarOrderable')
    for navbar in Navbar.objects.all():
        NavbarOrderable.create(navbar=navbar)
        NavbarOrderable.save()


def add_footer_orderables(apps, schema_editor):
    Footer = apps.get_model('coderedcms', 'Footer')
    FooterOrderable = apps.get_model('coderedcms', 'FooterOrderable')
    for footer in FooterOrderable.objects.all():
        FooterOrderable.create(footer=footer)
        FooterOrderable.save()


class Migration(migrations.Migration):

    dependencies = [
        ('coderedcms', '0020_footerorderable_navbarorderable'),
    ]

    operations = [
        migrations.RunPython(add_navbar_orderables),
        migrations.RunPython(add_footer_orderables)
    ]
