# Generated by Django 3.1.4 on 2021-03-31 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
