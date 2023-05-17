# Generated by Django 4.1.4 on 2023-04-05 11:35

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0051_sendmail_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendmail',
            name='status',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='profile/image/default.gif', upload_to=users.models.user_directory_path),
        ),
    ]
