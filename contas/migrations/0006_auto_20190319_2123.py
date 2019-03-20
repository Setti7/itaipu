# Generated by Django 2.1.5 on 2019-03-20 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0005_visitante_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitante',
            name='foto',
            field=models.ImageField(null=True, upload_to='fotos-visitantes/'),
        ),
        migrations.AlterField(
            model_name='visitante',
            name='veiculo',
            field=models.CharField(blank=True, db_column='veic_ID', max_length=7, null=True),
        ),
    ]