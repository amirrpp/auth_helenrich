# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('weblayout', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 'banners',
                'verbose_name_plural': 'Banners',
                'verbose_name': 'Banner',
            },
        ),
        migrations.CreateModel(
            name='BannerImagePosition',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('image_original', models.ImageField(upload_to='image_positions/banners/')),
                ('image_small', models.ImageField(blank=True, null=True, upload_to='image_positions/banners/')),
                ('image_medium', models.ImageField(blank=True, null=True, upload_to='image_positions/banners/')),
                ('image_large', models.ImageField(blank=True, null=True, upload_to='image_positions/banners/')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('title', models.CharField(max_length=256)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
                ('weight', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('description', models.CharField(blank=True, null=True, max_length=256)),
                ('banner', models.ForeignKey(to='website.Banner')),
            ],
            options={
                'db_table': 'banner_image_positions',
                'verbose_name_plural': 'Banner Image Positions',
                'verbose_name': 'Banner Image Position',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
                ('first_image', models.ImageField(blank=True, null=True, upload_to='galleries_covers/')),
                ('second_image', models.ImageField(blank=True, null=True, upload_to='galleries_covers/')),
            ],
            options={
                'db_table': 'galleries',
                'verbose_name_plural': 'Galleries',
                'verbose_name': 'Gallery',
            },
        ),
        migrations.CreateModel(
            name='GalleryImagePosition',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('image_original', models.ImageField(upload_to='image_positions/galleries/')),
                ('cropping_large', image_cropping.fields.ImageRatioField('image_original', '1200x800', help_text=None, free_crop=False, adapt_rotation=False, verbose_name='cropping large', allow_fullsize=False, hide_image_field=False, size_warning=False)),
                ('cropping_medium', image_cropping.fields.ImageRatioField('image_original', '750x230', help_text=None, free_crop=False, adapt_rotation=False, verbose_name='cropping medium', allow_fullsize=False, hide_image_field=False, size_warning=False)),
                ('cropping_small', image_cropping.fields.ImageRatioField('image_original', '62x44', help_text=None, free_crop=False, adapt_rotation=False, verbose_name='cropping small', allow_fullsize=False, hide_image_field=False, size_warning=False)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('title', models.CharField(max_length=256)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
                ('weight', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('description', models.CharField(blank=True, null=True, max_length=256)),
                ('gallery', models.ForeignKey(to='website.Gallery')),
            ],
            options={
                'db_table': 'gallery_image_positions',
                'verbose_name_plural': 'Gallery Image Positions',
                'verbose_name': 'Gallery Image Position',
            },
        ),
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('url', models.CharField(max_length=256, unique=True)),
                ('first_text', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('second_text', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('meta_description', models.CharField(blank=True, null=True, max_length=256)),
                ('title', models.CharField(max_length=256)),
                ('meta_canonical', models.CharField(blank=True, null=True, max_length=256)),
                ('meta_robots', models.CharField(blank=True, null=True, max_length=256)),
                ('h1', models.CharField(blank=True, null=True, max_length=256)),
                ('description', models.CharField(blank=True, null=True, max_length=256)),
                ('is_news', models.BooleanField()),
                ('first_image', models.ImageField(blank=True, null=True, upload_to='static_page/')),
                ('second_image', models.ImageField(blank=True, null=True, upload_to='static_page/')),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
                ('gallery', models.ForeignKey(to='website.Gallery', null=True, blank=True)),
                ('template', models.ForeignKey(to='weblayout.Template')),
            ],
            options={
                'db_table': 'static_pages',
                'verbose_name_plural': 'Static Pages',
                'verbose_name': 'Static Page',
            },
        ),
    ]
