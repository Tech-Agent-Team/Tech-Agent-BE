# Generated by Django 4.2.4 on 2023-08-28 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_order_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='location',
            field=models.CharField(default='Amman', max_length=255, null=True),
        ),
    ]
