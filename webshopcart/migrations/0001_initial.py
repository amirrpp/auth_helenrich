# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCart',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=256)),
                ('email', models.EmailField(blank=True, null=True, max_length=256)),
                ('phone', models.CharField(max_length=256)),
                ('description', models.TextField(max_length=256)),
                ('date_on_add', models.DateTimeField(auto_now_add=True)),
                ('date_on_close', models.DateTimeField(null=True, blank=True)),
                ('status', models.BooleanField(default=False)),
                ('fixed_sum', models.FloatField(null=True, blank=True)),
            ],
            options={
                'db_table': 'product_carts',
                'verbose_name_plural': 'Carts',
                'verbose_name': 'Cart',
            },
        ),
        migrations.CreateModel(
            name='ProductInCart',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('count', models.IntegerField()),
                ('cart', models.ForeignKey(to='webshopcart.ProductCart')),
                ('price_correction', smart_selects.db_fields.ChainedForeignKey(to='webshop.ProductPriceCorrector', auto_choose=True, null=True, chained_model_field='product', blank=True, chained_field='product')),
                ('product', models.ForeignKey(to='webshop.Product')),
            ],
            options={
                'db_table': 'products_in_carts',
                'verbose_name_plural': 'Products in Carts',
                'verbose_name': 'Product in Cart',
            },
        ),
    ]
