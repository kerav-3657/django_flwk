# Generated by Django 4.1.4 on 2023-03-18 11:45

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='profile/image/default.gif', upload_to=users.models.user_directory_path),
        ),
    ]
