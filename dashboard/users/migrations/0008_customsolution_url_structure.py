# Generated by Django 4.1.4 on 2023-03-17 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_orderproductimages_remove_orderprojectdata_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customsolution',
            name='url_structure',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
