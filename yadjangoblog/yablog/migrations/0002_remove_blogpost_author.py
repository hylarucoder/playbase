# Generated by Django 2.0 on 2018-01-30 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yablog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='author',
        ),
    ]
