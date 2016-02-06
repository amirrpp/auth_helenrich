# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalMenu',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('url', models.CharField(blank=True, null=True, default=None, max_length=256)),
                ('first_image', models.ImageField(blank=True, null=True, upload_to='additional_menu/')),
                ('second_image', models.ImageField(blank=True, null=True, upload_to='additional_menu/')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', null=True, to='weblayout.AdditionalMenu', blank=True)),
            ],
            options={
                'db_table': 'additional_menu',
                'verbose_name_plural': 'Additional Menu',
                'verbose_name': 'Additional Menu Element',
            },
        ),
        migrations.CreateModel(
            name='ExtraMenu',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('url', models.CharField(blank=True, null=True, default=None, max_length=256)),
                ('first_image', models.ImageField(blank=True, null=True, upload_to='extra_menu/')),
                ('second_image', models.ImageField(blank=True, null=True, upload_to='extra_menu/')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', null=True, to='weblayout.ExtraMenu', blank=True)),
            ],
            options={
                'db_table': 'extra_menu',
                'verbose_name_plural': 'Extra Menu',
                'verbose_name': 'Extra Menu Element',
            },
        ),
        migrations.CreateModel(
            name='MainMenu',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('url', models.CharField(blank=True, null=True, default=None, max_length=256)),
                ('first_image', models.ImageField(blank=True, null=True, upload_to='main_menu/')),
                ('second_image', models.ImageField(blank=True, null=True, upload_to='main_menu/')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', null=True, to='weblayout.MainMenu', blank=True)),
            ],
            options={
                'db_table': 'main_menu',
                'verbose_name_plural': 'Main Menu',
                'verbose_name': 'Main Menu Element',
            },
        ),
        migrations.CreateModel(
            name='SystemElement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=16, choices=[('Header', 'Header'), ('Footer', 'Footer'), ('Script', 'Script')], unique=True)),
                ('body', ckeditor.fields.RichTextField()),
            ],
            options={
                'db_table': 'system_elements',
                'verbose_name_plural': 'System Elements',
                'verbose_name': 'System Element',
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('path', models.CharField(max_length=256, unique=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 'templates',
                'verbose_name_plural': 'Templates',
                'verbose_name': 'Template',
            },
        ),
    ]
