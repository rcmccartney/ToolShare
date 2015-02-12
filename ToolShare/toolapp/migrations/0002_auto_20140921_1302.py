# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('toolapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tool',
            name='email',
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, default='temp@temp.com'),
            preserve_default=False,
        ),
    ]
