# Generated by Django 2.0.7 on 2018-08-29 19:38

import coderedcms.blocks.base_blocks
import coderedcms.fields
from django.db import migrations, models
import wagtail.contrib.table_block.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.documents.blocks
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('coderedcms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentWall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('content', coderedcms.fields.CoderedStreamField([], blank=True, verbose_name='Content')),
                ('is_dismissible', models.BooleanField(default=True, verbose_name='Dismissible')),
                ('show_once', models.BooleanField(default=True, help_text='Do not show the content wall to the same user again after it has been closed.', verbose_name='Show once')),
            ],
            options={
                'verbose_name': 'Content Wall',
            },
        ),
        migrations.AddField(
            model_name='coderedpage',
            name='content_walls',
            field=coderedcms.fields.CoderedStreamField([], blank=True, verbose_name='Content Walls'),
        ),
    ]
