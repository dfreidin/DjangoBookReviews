# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-18 05:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='stars',
            new_name='rating',
        ),
        migrations.RemoveField(
            model_name='book',
            name='uploader',
        ),
    ]
