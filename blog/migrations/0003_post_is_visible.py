# Generated by Django 3.2.5 on 2021-12-08 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
    ]