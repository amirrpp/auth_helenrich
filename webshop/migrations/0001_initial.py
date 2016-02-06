# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields
import ckeditor.fields
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('weblayout', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('url', models.CharField(max_length=256, unique=True)),
                ('title', models.CharField(max_length=256)),
                ('first_text', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('second_text', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('meta_description', models.CharField(blank=True, null=True, max_length=256)),
                ('meta_canonical', models.CharField(blank=True, null=True, max_length=256)),
                ('meta_robots', models.CharField(blank=True, null=True, max_length=256)),
                ('h1', models.CharField(blank=True, null=True, max_length=256)),
                ('description', models.CharField(blank=True, null=True, max_length=256)),
                ('first_image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('second_image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
                ('title_generation_rule', models.CharField(blank=True, null=True, max_length=256)),
                ('meta_description_generation_rule', models.CharField(blank=True, null=True, max_length=256)),
                ('h1_generation_rule', models.CharField(blank=True, null=True, max_length=256)),
                ('template', models.ForeignKey(to='weblayout.Template')),
            ],
            options={
                'db_table': 'categories',
                'verbose_name_plural': 'Categories',
                'verbose_name': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('short_name', models.CharField(max_length=3)),
            ],
            options={
                'db_table': 'currencies',
                'verbose_name_plural': 'Currencies',
                'verbose_name': 'Currency',
            },
        ),
        migrations.CreateModel(
            name='DeliveryRule',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('from_mass', models.FloatField(null=True, blank=True)),
                ('to_mass', models.FloatField(null=True, blank=True)),
                ('price', models.FloatField()),
            ],
            options={
                'db_table': 'delivery_rules',
                'verbose_name_plural': 'Delivery Rules',
                'verbose_name': 'Delivery Rule',
            },
        ),
        migrations.CreateModel(
            name='Margin',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('percent', models.FloatField()),
            ],
            options={
                'db_table': 'margins',
                'verbose_name_plural': 'Margins',
                'verbose_name': 'Margin',
            },
        ),
        migrations.CreateModel(
            name='PreFilter',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('price_from', models.FloatField()),
                ('price_to', models.FloatField()),
                ('order', models.CharField(max_length=256, choices=[('by weight', 'by weight'), ('by price asc', 'by price asc'), ('by price dsc', 'by price dsc'), ('by date', 'by date')])),
                ('category', models.ForeignKey(to='webshop.Category')),
            ],
            options={
                'db_table': 'pre_filters',
                'verbose_name_plural': 'PreFilters',
                'verbose_name': 'PreFilter',
            },
        ),
        migrations.CreateModel(
            name='PreFilterParameterValue',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('custom_value', models.CharField(blank=True, null=True, max_length=256)),
                ('category', models.ForeignKey(to='webshop.Category')),
                ('pre_filter', models.ForeignKey(to='webshop.PreFilter')),
            ],
            options={
                'db_table': 'pre_filter_parameters_value',
                'verbose_name_plural': 'PreFilter Parameter Values',
                'verbose_name': 'PreFilter Parameter Value',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('code', models.CharField(max_length=256, unique=True)),
                ('url', models.CharField(max_length=256, unique=True)),
                ('title', models.CharField(blank=True, null=True, max_length=256)),
                ('default_price', models.FloatField()),
                ('active', models.BooleanField(default=True)),
                ('first_text', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('second_text', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('meta_description', models.CharField(blank=True, null=True, max_length=256)),
                ('meta_canonical', models.CharField(blank=True, null=True, max_length=256)),
                ('meta_robots', models.CharField(blank=True, null=True, max_length=256)),
                ('h1', models.CharField(blank=True, null=True, max_length=256)),
                ('description', models.CharField(blank=True, null=True, max_length=256)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
                ('weight', models.IntegerField(default=0)),
                ('mass', models.FloatField(default=0)),
                ('category', models.ForeignKey(to='webshop.Category')),
                ('margin', models.ForeignKey(to='webshop.Margin', null=True, blank=True)),
            ],
            options={
                'db_table': 'products',
                'verbose_name_plural': 'Products',
                'verbose_name': 'Product',
            },
        ),
        migrations.CreateModel(
            name='ProductImagePosition',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('image_original', models.ImageField(upload_to='image_positions/products/')),
                ('cropping_large', image_cropping.fields.ImageRatioField('image_original', '960x680', help_text=None, free_crop=False, adapt_rotation=False, verbose_name='cropping large', allow_fullsize=False, hide_image_field=False, size_warning=False)),
                ('cropping_medium', image_cropping.fields.ImageRatioField('image_original', '162x122', help_text=None, free_crop=False, adapt_rotation=False, verbose_name='cropping medium', allow_fullsize=False, hide_image_field=False, size_warning=False)),
                ('cropping_small', image_cropping.fields.ImageRatioField('image_original', '62x44', help_text=None, free_crop=False, adapt_rotation=False, verbose_name='cropping small', allow_fullsize=False, hide_image_field=False, size_warning=False)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('title', models.CharField(max_length=256)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
                ('weight', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('description', models.CharField(blank=True, null=True, max_length=256)),
                ('product', models.ForeignKey(to='webshop.Product')),
            ],
            options={
                'db_table': 'product_image_positions',
                'verbose_name_plural': 'Product Image Positions',
                'verbose_name': 'Product Image Position',
            },
        ),
        migrations.CreateModel(
            name='ProductParameter',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('sort_as', models.CharField(max_length=32, choices=[('BOOLEAN', 'BOOLEAN'), ('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('FLOAT', 'FLOAT')])),
                ('first_image', models.ImageField(blank=True, null=True, upload_to='product_parameter/')),
                ('second_image', models.ImageField(blank=True, null=True, upload_to='product_parameter/')),
                ('prefix', models.CharField(blank=True, null=True, max_length=8)),
                ('suffix', models.CharField(blank=True, null=True, max_length=8)),
                ('weight', models.IntegerField()),
                ('category', models.ForeignKey(to='webshop.Category')),
            ],
            options={
                'db_table': 'product_parameters',
                'verbose_name_plural': 'Product Parameters',
                'verbose_name': 'Product Parameter',
            },
        ),
        migrations.CreateModel(
            name='ProductParameterAvailableInterval',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('from_value', models.FloatField(null=True, blank=True)),
                ('to_value', models.FloatField(null=True, blank=True)),
                ('product_parameter', models.ForeignKey(to='webshop.ProductParameter')),
            ],
            options={
                'db_table': 'product_parameters_available_intervals',
                'verbose_name_plural': 'Product Parameter Available Intervals',
                'verbose_name': 'Product Parameter Available Interval',
            },
        ),
        migrations.CreateModel(
            name='ProductParameterAvailableValue',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('value', models.CharField(max_length=256)),
                ('product_parameter', models.ForeignKey(to='webshop.ProductParameter')),
            ],
            options={
                'db_table': 'product_parameters_available_value',
                'verbose_name_plural': 'Product Parameter Available Values',
                'verbose_name': 'Product Parameter Available Value',
            },
        ),
        migrations.CreateModel(
            name='ProductParameterValue',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('custom_value', models.CharField(blank=True, null=True, max_length=256)),
                ('category', models.ForeignKey(to='webshop.Category')),
                ('product', models.ForeignKey(to='webshop.Product')),
                ('product_parameter', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='category', chained_model_field='category', to='webshop.ProductParameter')),
                ('value', smart_selects.db_fields.ChainedForeignKey(to='webshop.ProductParameterAvailableValue', auto_choose=True, null=True, chained_model_field='product_parameter', blank=True, chained_field='product_parameter')),
            ],
            options={
                'db_table': 'product_parameters_values',
                'verbose_name_plural': 'Product Parameter Values',
                'verbose_name': 'Product Parameter Value',
            },
        ),
        migrations.CreateModel(
            name='ProductPriceCorrector',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('new_price', models.FloatField()),
                ('product', models.ForeignKey(to='webshop.Product')),
            ],
            options={
                'db_table': 'product_price_correctors',
                'verbose_name_plural': 'Product Price Corrections',
                'verbose_name': 'Product Price Correction',
            },
        ),
        migrations.CreateModel(
            name='ProductRating',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('user_name', models.CharField(max_length=256)),
                ('email', models.CharField(max_length=256)),
                ('comment', ckeditor.fields.RichTextField()),
                ('rating', models.FloatField()),
                ('state', models.BooleanField(default=False)),
                ('date_on_add', models.DateField(auto_now=True)),
                ('product', models.ForeignKey(to='webshop.Product')),
            ],
            options={
                'db_table': 'product_ratings',
                'verbose_name_plural': 'Rating and comment for product',
                'verbose_name': 'Ratings and comments for product',
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('coefficient', models.FloatField()),
                ('currency', models.ForeignKey(to='webshop.Currency')),
            ],
            options={
                'db_table': 'providers',
                'verbose_name_plural': 'Providers',
                'verbose_name': 'Provider',
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('percent', models.FloatField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='sales/')),
            ],
            options={
                'db_table': 'sales',
                'verbose_name_plural': 'Sales',
                'verbose_name': 'Sale',
            },
        ),
        migrations.CreateModel(
            name='SpecialProposition',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='special_propositions/')),
            ],
            options={
                'db_table': 'special_propositions',
                'verbose_name_plural': 'Special Propositions',
                'verbose_name': 'Special Proposition',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='provider',
            field=models.ForeignKey(to='webshop.Provider'),
        ),
        migrations.AddField(
            model_name='product',
            name='sale',
            field=models.ForeignKey(to='webshop.Sale', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='special_proposition',
            field=models.ForeignKey(to='webshop.SpecialProposition', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='template',
            field=models.ForeignKey(to='weblayout.Template'),
        ),
        migrations.AddField(
            model_name='prefilterparametervalue',
            name='product_parameter',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='category', chained_model_field='category', to='webshop.ProductParameter'),
        ),
        migrations.AddField(
            model_name='prefilterparametervalue',
            name='value',
            field=smart_selects.db_fields.ChainedForeignKey(to='webshop.ProductParameterAvailableValue', auto_choose=True, null=True, chained_model_field='product_parameter', blank=True, chained_field='product_parameter'),
        ),
        migrations.AddField(
            model_name='prefilterparametervalue',
            name='value_interval',
            field=smart_selects.db_fields.ChainedForeignKey(to='webshop.ProductParameterAvailableInterval', auto_choose=True, null=True, chained_model_field='product_parameter', blank=True, chained_field='product_parameter'),
        ),
        migrations.AlterUniqueTogether(
            name='productparametervalue',
            unique_together=set([('product', 'category', 'product_parameter')]),
        ),
        migrations.AlterUniqueTogether(
            name='productparameteravailablevalue',
            unique_together=set([('product_parameter', 'value')]),
        ),
        migrations.AlterUniqueTogether(
            name='productparameteravailableinterval',
            unique_together=set([('name', 'product_parameter')]),
        ),
        migrations.AlterUniqueTogether(
            name='productparameter',
            unique_together=set([('name', 'category')]),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('name', 'category')]),
        ),
        migrations.AlterUniqueTogether(
            name='prefilterparametervalue',
            unique_together=set([('pre_filter', 'product_parameter')]),
        ),
    ]
