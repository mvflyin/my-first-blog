# Generated by Django 2.2.6 on 2019-10-18 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20191018_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='short_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]