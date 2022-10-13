# Generated by Django 4.1 on 2022-09-03 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferumbel', '0051_alter_characteristic_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='ferumbel.category', verbose_name='Категория'),
        ),
    ]
