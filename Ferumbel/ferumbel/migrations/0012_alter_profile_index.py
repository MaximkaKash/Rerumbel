# Generated by Django 3.2.9 on 2022-01-06 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferumbel', '0011_profile_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='index',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
