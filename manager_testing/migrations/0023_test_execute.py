# Generated by Django 3.0.3 on 2020-02-19 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_testing', '0022_remove_test_execute'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='execute',
            field=models.BooleanField(default=False),
        ),
    ]
