from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


def add_navbar_orderables(apps, schema_editor):
    Site = apps.get_model('wagtailcore', 'Site')
    LayoutSettings = apps.get_model('coderedcms', 'LayoutSettings')
    Navbar = apps.get_model('coderedcms', 'Navbar')
    NavbarOrderable = apps.get_model('coderedcms', 'NavbarOrderable')
    # If it's a new site, this migration will not run.
    try:
        site = Site.objects.get(is_default_site=True)
        layout = LayoutSettings.objects.get(site=site)
    except (Site.DoesNotExist, LayoutSettings.DoesNotExist):
        return
    current_navs = Navbar.objects.all()
    db_alias = schema_editor.connection.alias
    layout.site_navbar = []
    layout.save()
    for nav in current_navs:
        NavbarOrderable.objects.using(db_alias).create(navbar_chooser=layout, navbar=nav)


def add_footer_orderables(apps, schema_editor):
    Site = apps.get_model('wagtailcore', 'Site')
    LayoutSettings = apps.get_model('coderedcms', 'LayoutSettings')
    Footer = apps.get_model('coderedcms', 'Footer')
    FooterOrderable = apps.get_model('coderedcms', 'FooterOrderable')
    # If it's a new site, this migration will not run.
    try:
        site = Site.objects.get(is_default_site=True)
        layout = LayoutSettings.objects.get(site=site)
    except (Site.DoesNotExist, LayoutSettings.DoesNotExist):
        return
    current_footers = Footer.objects.all()
    db_alias = schema_editor.connection.alias
    layout.site_footer = []
    layout.save()
    for footer in current_footers:
        FooterOrderable.objects.using(db_alias).create(footer_chooser=layout, footer=footer)


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('coderedcms', '0028_auto_20220609_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavbarOrderable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('navbar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coderedcms.navbar')),
                ('navbar_chooser', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='site_navbar', to='coderedcms.layoutsettings', verbose_name='Site Navbars')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FooterOrderable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('footer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coderedcms.footer')),
                ('footer_chooser', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='site_footer', to='coderedcms.layoutsettings', verbose_name='Site Footers')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.RunPython(add_navbar_orderables),
        migrations.RunPython(add_footer_orderables)
    ]
