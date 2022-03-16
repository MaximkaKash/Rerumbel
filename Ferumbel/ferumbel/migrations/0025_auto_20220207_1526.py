# Generated by Django 3.2.9 on 2022-02-07 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ferumbel', '0024_alter_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='code',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ferumbel.customer'),
        ),
    ]