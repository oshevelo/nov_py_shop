# Generated by Django 2.2.4 on 2020-01-24 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20200124_1321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user_address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user_phone',
        ),
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.CharField(max_length=500),
        ),
    ]
