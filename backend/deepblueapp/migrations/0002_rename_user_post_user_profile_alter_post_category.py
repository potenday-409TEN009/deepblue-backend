# Generated by Django 5.1.1 on 2024-10-02 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deepblueapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user',
            new_name='user_profile',
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('a', 'A'), ('b', 'B'), ('c', 'C')], max_length=5),
        ),
    ]
