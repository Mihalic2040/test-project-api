# Generated by Django 4.1.5 on 2023-02-09 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='onwer',
            new_name='owner',
        ),
    ]
