# Generated by Django 3.2.9 on 2022-03-09 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferumbel', '0029_auto_20220309_1331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='separation',
        ),
        migrations.AddField(
            model_name='product',
            name='division',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Разделение'),
        ),
        migrations.DeleteModel(
            name='Division',
        ),
    ]
