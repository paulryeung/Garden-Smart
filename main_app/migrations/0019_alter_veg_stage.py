# Generated by Django 4.0.6 on 2022-07-28 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0018_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='veg',
            name='stage',
            field=models.CharField(choices=[('S', 'Seeded'), ('G', 'Growth'), ('H', 'Harvest')], default='S', max_length=1),
        ),
    ]