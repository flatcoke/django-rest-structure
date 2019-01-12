# Generated by Django 2.1.2 on 2019-01-07 16:33

import sys
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='provider',
            field=models.CharField(default='email', max_length=30,
                                   verbose_name='provider'),
        ),
        migrations.AddField(
            model_name='user',
            name='uid',
            field=models.CharField(default=None, max_length=255,
                                   verbose_name='uid'),
        ),
    ]
    if 'test' not in sys.argv and 'test_coverage' not in sys.argv:
        operations += [
            migrations.RunSQL([
                ("alter table users modify "
                 "column provider varchar(30) after password"),
                ("alter table users modify "
                 "column uid varchar(255) after provider"),
            ], ''  # this is not effect to other sql
            ),
        ]