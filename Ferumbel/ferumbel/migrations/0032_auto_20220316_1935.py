# Generated by Django 3.2.9 on 2022-03-16 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferumbel', '0031_alter_product_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='ID',
        ),
        migrations.AddField(
            model_name='customer',
            name='foruser',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
