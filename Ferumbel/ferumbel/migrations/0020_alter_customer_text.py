# Generated by Django 3.2.9 on 2022-01-27 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferumbel', '0019_auto_20220127_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='Text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
