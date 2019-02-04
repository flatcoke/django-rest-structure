# Generated by Django 2.1.2 on 2019-02-04 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190107_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, verbose_name='username'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['username'], name='idx_users_username'),
        ),
    ]
