# Generated by Django 3.0.3 on 2020-02-19 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_testing', '0019_testplanresult_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testplanresult',
            name='shipment_id',
        ),
        migrations.AddField(
            model_name='testplan',
            name='response_type',
            field=models.CharField(blank=True, choices=[('PDF', 'PDF'), ('ZPL2', 'ZPL')], max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='testplan',
            name='shipment_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
