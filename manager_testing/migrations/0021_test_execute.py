# Generated by Django 3.0.3 on 2020-02-19 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_testing', '0020_auto_20200219_0259'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='execute',
            field=models.BooleanField(default=False),
        ),
    ]
