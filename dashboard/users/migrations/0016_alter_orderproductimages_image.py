# Generated by Django 4.1.4 on 2023-03-18 11:11

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_remove_orderproductimages_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproductimages',
            name='image',
            field=models.ImageField(default='profile/image/default.gif', upload_to=users.models.user_directory_path),
        ),
    ]
