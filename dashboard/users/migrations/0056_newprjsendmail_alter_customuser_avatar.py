# Generated by Django 4.1.4 on 2023-04-21 13:17

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0055_draftsendmail_message_alter_customuser_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewPrjsendMail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution_name', models.CharField(blank=True, max_length=255)),
                ('number_of_audit', models.CharField(blank=True, max_length=255)),
                ('started_date', models.CharField(blank=True, max_length=255)),
                ('message', models.CharField(blank=True, max_length=255)),
                ('name', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='profile/image/default.gif', upload_to=users.models.user_directory_path),
        ),
    ]
