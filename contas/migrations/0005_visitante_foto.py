# Generated by Django 2.1.5 on 2019-03-18 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0004_auto_20181214_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitante',
            name='foto',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
