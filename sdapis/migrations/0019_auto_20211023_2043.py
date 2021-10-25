# Generated by Django 3.2.8 on 2021-10-24 02:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sdapis', '0018_auto_20211023_1446'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_id',
        ),
        migrations.AddField(
            model_name='post',
            name='id',
            field=models.CharField(default=uuid.uuid4, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
