# Generated by Django 4.2.3 on 2024-03-09 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_cart_rice_images_rice_price_cartitems'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitems',
            old_name='pizza',
            new_name='rice',
        ),
    ]
