# Generated by Django 4.1.5 on 2023-02-01 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_user_is_active_alter_user_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
    ]