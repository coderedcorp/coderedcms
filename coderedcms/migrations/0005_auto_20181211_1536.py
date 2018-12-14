# Generated by Django 2.0.9 on 2018-12-11 20:36

import coderedcms.blocks.base_blocks
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('coderedcms', '0004_auto_20181119_1507'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoderedTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='coderedcms.CoderedPage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coderedcms_coderedtag_items', to='taggit.Tag')),
            ],
            options={
                'verbose_name': 'CodeRed Tag',
            },
        ),
        migrations.AddField(
            model_name='coderedpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='Used to categorize your pages.', through='coderedcms.CoderedTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
