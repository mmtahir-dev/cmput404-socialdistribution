# Generated by Django 3.2.8 on 2021-10-22 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdapis', '0012_post_comment_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author_id',
            field=models.CharField(default='no author', max_length=100),
        ),
    ]
