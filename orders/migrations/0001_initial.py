# Generated by Django 4.1.5 on 2023-08-31 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '__first__'),
        ('technician', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField()),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('state_is_ongoing', models.BooleanField(default=False)),
                ('state_show', models.BooleanField(default=True)),
                ('eta_arrival_time', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField()),
                ('technician_type', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('address', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('location', models.CharField(blank=True, default='Some Default Location', max_length=255, null=True)),
                ('current_technician', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='technician.technicianprofile')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customerprofile')),
            ],
        ),
        migrations.AlterField(
            model_name='Order',
            name='eta_arrival_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('sender', models.CharField(max_length=255, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='orders.order')),
            ],
        ),
    ]
