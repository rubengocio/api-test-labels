# Generated by Django 3.0.3 on 2020-02-19 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_testing', '0009_auto_20200219_0137'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrier',
            name='code',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='code',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
    ]
