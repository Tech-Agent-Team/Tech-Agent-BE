# Generated by Django 4.2.4 on 2023-08-28 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_eta_arrival_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='eta_arrival_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]