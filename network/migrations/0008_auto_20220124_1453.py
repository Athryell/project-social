# Generated by Django 3.2.5 on 2022-01-24 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_auto_20220123_1448'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='follower',
            new_name='following',
        ),
        migrations.RemoveField(
            model_name='user',
            name='followed',
        ),
    ]
