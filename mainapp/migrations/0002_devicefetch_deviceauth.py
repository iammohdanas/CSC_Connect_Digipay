# Generated by Django 4.2.5 on 2024-03-07 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceFetch',
            fields=[
                ('port', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=20)),
                ('info', models.CharField(max_length=200)),
                ('method_capture', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceAuth',
            fields=[
                ('csc_id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('device_id', models.CharField(max_length=100)),
                ('hmac', models.CharField(max_length=20)),
                ('port', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authentications', to='mainapp.devicefetch')),
            ],
        ),
    ]
