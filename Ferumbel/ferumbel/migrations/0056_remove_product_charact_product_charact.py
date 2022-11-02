# Generated by Django 4.1 on 2022-09-03 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ferumbel', '0055_alter_product_charact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='charact',
        ),
        migrations.AddField(
            model_name='product',
            name='charact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ferumbel.characteristic', verbose_name='Характеристика'),
        ),
    ]