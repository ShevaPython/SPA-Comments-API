# Generated by Django 4.2.7 on 2023-11-27 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='home_page',
            field=models.URLField(blank=True),
        ),
    ]
