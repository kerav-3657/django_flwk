# Generated by Django 4.1.4 on 2023-03-21 12:37

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0037_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='profile/image/default.gif', upload_to=users.models.user_directory_path),
        ),
    ]
