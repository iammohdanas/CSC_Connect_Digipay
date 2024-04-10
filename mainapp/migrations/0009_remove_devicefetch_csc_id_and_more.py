# Generated by Django 4.2.5 on 2024-04-09 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_remove_deviceauth_port'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicefetch',
            name='csc_id',
        ),
        migrations.RemoveField(
            model_name='devicefetch',
            name='device_id',
        ),
        migrations.AddField(
            model_name='deviceauth',
            name='port',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='authentications', to='mainapp.devicefetch'),
        ),
        migrations.AddField(
            model_name='devicefetch',
            name='method_capture',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='devicefetch',
            name='port',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='devicefetch',
            name='csc_Id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]