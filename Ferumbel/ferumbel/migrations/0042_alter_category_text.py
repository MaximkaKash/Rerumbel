# Generated by Django 3.2.9 on 2022-04-27 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferumbel', '0041_alter_category_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='Text',
            field=models.TextField(blank=True, verbose_name='Название'),
        ),
    ]
