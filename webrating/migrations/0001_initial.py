# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('user_name', models.CharField(max_length=256)),
                ('email', models.CharField(blank=True, null=True, max_length=256)),
                ('comment', ckeditor.fields.RichTextField()),
                ('rating', models.FloatField()),
                ('state', models.BooleanField(default=False)),
                ('date_on_add', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 'ratings',
                'verbose_name_plural': 'Ratings and comments',
                'verbose_name': 'Comment',
            },
        ),
    ]
