# Generated by Django 4.1 on 2022-10-13 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferumbel', '0058_curs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='coefficient',
            field=models.FloatField(default=1, verbose_name='Коэффициент'),
        ),
    ]
