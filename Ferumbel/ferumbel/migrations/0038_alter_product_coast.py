# Generated by Django 3.2.9 on 2022-04-11 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferumbel', '0037_remove_product_html_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='coast',
            field=models.IntegerField(blank=True, null=True, verbose_name='Цена'),
        ),
    ]