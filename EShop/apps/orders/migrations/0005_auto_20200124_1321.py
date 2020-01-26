# Generated by Django 2.2.4 on 2020-01-24 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('orders', '0004_order_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user_address',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='users.UserAddress'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='user_phone',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.UserPhone'),
            preserve_default=False,
        ),
    ]
