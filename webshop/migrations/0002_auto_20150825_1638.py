# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productparameteravailableinterval',
            name='first_image',
            field=models.ImageField(null=True, blank=True, upload_to='product_parameter_interval/'),
        ),
        migrations.AddField(
            model_name='productparameteravailableinterval',
            name='second_image',
            field=models.ImageField(null=True, blank=True, upload_to='product_parameter_interval/'),
        ),
        migrations.AddField(
            model_name='productparameteravailableinterval',
            name='weight',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productparameteravailablevalue',
            name='first_image',
            field=models.ImageField(null=True, blank=True, upload_to='product_parameter_value/'),
        ),
        migrations.AddField(
            model_name='productparameteravailablevalue',
            name='second_image',
            field=models.ImageField(null=True, blank=True, upload_to='product_parameter_value/'),
        ),
        migrations.AddField(
            model_name='productparameteravailablevalue',
            name='weight',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='cropping_large',
            field=image_cropping.fields.ImageRatioField('image_original', '340x440', help_text=None, hide_image_field=False, size_warning=False, free_crop=False, adapt_rotation=False, verbose_name='cropping large', allow_fullsize=False),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='cropping_medium',
            field=image_cropping.fields.ImageRatioField('image_original', '260x330', help_text=None, hide_image_field=False, size_warning=False, free_crop=False, adapt_rotation=False, verbose_name='cropping medium', allow_fullsize=False),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='cropping_small',
            field=image_cropping.fields.ImageRatioField('image_original', '155x190', help_text=None, hide_image_field=False, size_warning=False, free_crop=False, adapt_rotation=False, verbose_name='cropping small', allow_fullsize=False),
        ),
    ]
