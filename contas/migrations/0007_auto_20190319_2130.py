# Generated by Django 2.1.5 on 2019-03-20 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0006_auto_20190319_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitante',
            name='foto',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
