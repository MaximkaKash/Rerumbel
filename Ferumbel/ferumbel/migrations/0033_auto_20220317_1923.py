# Generated by Django 3.2.9 on 2022-03-17 19:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ferumbel', '0032_auto_20220316_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='pole',
            field=models.TextField(null=True, verbose_name='Поле'),
        ),
        migrations.AlterField(
            model_name='order',
            name='adress',
            field=models.TextField(blank=True, null=True, verbose_name='Адрес доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='coast',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ferumbel.customer', verbose_name='Продавец'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery',
            field=models.BooleanField(blank=True, null=True, verbose_name='Необходима ли доставка'),
        ),
        migrations.AlterField(
            model_name='order',
            name='index',
            field=models.IntegerField(blank=True, null=True, verbose_name='Индекс покупателя'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='order',
            name='purchase',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ferumbel.purchase', verbose_name='Корзина'),
        ),
        migrations.AlterField(
            model_name='order',
            name='statuc',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='count',
            field=models.IntegerField(verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='index',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='Индекс пользователя'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='ferumbel.product', verbose_name='Продукт'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
