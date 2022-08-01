# Generated by Django 4.0.6 on 2022-08-01 15:09

import coderedcms.fields
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('coderedcms', '0030_alter_coderedtag_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accordion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Accordion',
                'verbose_name_plural': 'Accordions',
            },
        ),
        migrations.CreateModel(
            name='AccordionPanel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('content', coderedcms.fields.CoderedStreamField(blank=True)),
                ('custom_css_class', models.CharField(blank=True, max_length=255, verbose_name='Custom CSS class')),
                ('custom_id', models.CharField(blank=True, max_length=255, verbose_name='Custom ID')),
                ('accordion', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='accordion_panels', to='coderedcms.accordion', verbose_name='Accordion')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
