# Generated by Django 5.2.1 on 2025-06-11 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_rename_products_productss'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Productss',
            new_name='Product',
        ),
    ]
