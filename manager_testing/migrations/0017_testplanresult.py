# Generated by Django 3.0.3 on 2020-02-19 02:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager_testing', '0016_remove_testplan_shipment_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestPlanResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipment_id', models.BigIntegerField(blank=True, null=True)),
                ('result', models.BooleanField(default=False)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager_testing.Test')),
                ('test_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager_testing.TestPlan')),
            ],
        ),
    ]
