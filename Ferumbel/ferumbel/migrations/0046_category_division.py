# Generated by Django 3.2.9 on 2022-07-25 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferumbel', '0045_auto_20220511_0714'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='division',
            field=models.BooleanField(default=True, verbose_name='Разделение'),
        ),
    ]
