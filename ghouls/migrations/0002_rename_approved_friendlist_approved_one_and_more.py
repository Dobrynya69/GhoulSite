# Generated by Django 4.1.3 on 2022-11-17 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ghouls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendlist',
            old_name='approved',
            new_name='approved_one',
        ),
        migrations.AddField(
            model_name='friendlist',
            name='approved_two',
            field=models.BooleanField(default=False),
        ),
    ]
