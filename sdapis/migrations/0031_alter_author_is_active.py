# Generated by Django 3.2.8 on 2021-10-29 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdapis', '0030_alter_post_visibility'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]