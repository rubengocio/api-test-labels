# Generated by Django 3.0.3 on 2020-02-24 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager_testing', '0033_auto_20200224_0406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testplanresult',
            name='image_production',
        ),
        migrations.RemoveField(
            model_name='testplanresult',
            name='image_test',
        ),
        migrations.RemoveField(
            model_name='testplanresult',
            name='result',
        ),
    ]
