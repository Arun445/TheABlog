# Generated by Django 3.1.7 on 2021-04-04 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20210404_0109'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='about',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
