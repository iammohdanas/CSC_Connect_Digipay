# Generated by Django 4.2.5 on 2024-04-09 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_remove_devicefetch_method_capture_devicefetch_csc_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicefetch',
            name='csc_Id',
        ),
        migrations.RemoveField(
            model_name='devicefetch',
            name='id',
        ),
        migrations.RemoveField(
            model_name='devicefetch',
            name='mac',
        ),
        migrations.RemoveField(
            model_name='devicefetch',
            name='purpose',
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
    ]
