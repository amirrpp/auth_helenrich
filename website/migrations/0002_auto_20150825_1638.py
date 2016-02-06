# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryimageposition',
            name='cropping_medium',
            field=image_cropping.fields.ImageRatioField('image_original', '1200x494', help_text=None, hide_image_field=False, size_warning=False, free_crop=False, adapt_rotation=False, verbose_name='cropping medium', allow_fullsize=False),
        ),
    ]
