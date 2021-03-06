# Generated by Django 3.1.4 on 2021-05-15 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('civictechprojects', '0044_volunteerrelation_is_team_leader'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectposition',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='projectposition',
            name='order_number',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
