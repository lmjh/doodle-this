# Generated by Django 3.2 on 2022-06-20 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_orderdrawing_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address_2',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='county',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
