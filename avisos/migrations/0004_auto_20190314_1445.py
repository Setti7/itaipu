# Generated by Django 2.1.5 on 2019-03-14 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avisos', '0003_auto_20190314_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='aviso',
            name='subtitulo',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='sub-título'),
        ),
        migrations.AlterField(
            model_name='aviso',
            name='titulo',
            field=models.CharField(max_length=100, verbose_name='título'),
        ),
    ]
