# Generated by Django 4.1.4 on 2023-03-21 10:47

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0032_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='profile/image/default.gif', upload_to=users.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='orderproductimages',
            name='image',
            field=models.ImageField(default=0.0, upload_to='order_product_images/'),
        ),
    ]
