# Generated by Django 4.2.7 on 2024-01-18 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0008_alter_order_created_at_alter_order_delivery_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='updated_at',
            field=models.DateField(auto_now=True, null=True, verbose_name='дата обновления информации о товаре'),
        ),
    ]
