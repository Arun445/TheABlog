# Generated by Django 3.1.7 on 2021-04-04 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210404_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pictures'),
        ),
    ]
