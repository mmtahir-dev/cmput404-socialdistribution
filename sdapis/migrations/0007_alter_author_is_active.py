# Generated by Django 3.2.8 on 2021-10-19 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdapis', '0006_alter_author_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
