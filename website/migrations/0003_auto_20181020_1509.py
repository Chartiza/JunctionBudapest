# Generated by Django 2.0.8 on 2018-10-20 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20181020_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snp',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]