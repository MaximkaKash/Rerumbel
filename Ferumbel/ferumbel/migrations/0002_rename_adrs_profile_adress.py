# Generated by Django 3.2.9 on 2021-12-05 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ferumbel', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='adrs',
            new_name='adress',
        ),
    ]
