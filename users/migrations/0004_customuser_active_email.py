# Generated by Django 4.1.3 on 2022-11-13 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_zxc_level_alter_customuser_zxc_scores'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='active_email',
            field=models.BooleanField(default=False),
        ),
    ]