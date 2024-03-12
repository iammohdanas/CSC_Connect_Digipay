# Generated by Django 4.2.5 on 2024-03-11 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_devicefetch_deviceauth'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=100, null=True)),
                ('purpose', models.CharField(max_length=300, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='devicefetch',
            name='dc',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='devicefetch',
            name='mi',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='deviceauth',
            name='device_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='deviceauth',
            name='hmac',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='deviceauth',
            name='port',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='authentications', to='mainapp.devicefetch'),
        ),
        migrations.AlterField(
            model_name='devicefetch',
            name='info',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='devicefetch',
            name='method_capture',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='devicefetch',
            name='status',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
