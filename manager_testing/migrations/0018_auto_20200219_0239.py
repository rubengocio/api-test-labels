# Generated by Django 3.0.3 on 2020-02-19 02:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager_testing', '0017_testplanresult'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testplanresult',
            old_name='result',
            new_name='pass_test',
        ),
    ]
