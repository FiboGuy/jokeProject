# Generated by Django 2.1.7 on 2019-03-30 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0007_auto_20190323_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
