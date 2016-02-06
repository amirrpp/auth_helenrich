# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0002_auto_20150825_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='prefilter',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='prefilter',
            name='description',
            field=models.CharField(null=True, blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='prefilter',
            name='first_text',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='prefilter',
            name='h1',
            field=models.CharField(null=True, blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='prefilter',
            name='meta_canonical',
            field=models.CharField(null=True, blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='prefilter',
            name='meta_description',
            field=models.CharField(null=True, blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='prefilter',
            name='meta_robots',
            field=models.CharField(null=True, blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='prefilter',
            name='second_text',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='prefilter',
            name='title',
            field=models.CharField(null=True, blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='prefilter',
            name='url',
            field=models.CharField(unique=True, default=1, max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='prefilter',
            name='price_from',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prefilter',
            name='price_to',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
