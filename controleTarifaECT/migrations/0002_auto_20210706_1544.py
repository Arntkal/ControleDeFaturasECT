# Generated by Django 3.2.5 on 2021-07-06 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controleTarifaECT', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TT_codigoTarifaECT',
            new_name='CodigoTarifa',
        ),
        migrations.RenameModel(
            old_name='TT_tarifaECT',
            new_name='Tarifa',
        ),
        migrations.RenameField(
            model_name='tarifa',
            old_name='idTT_tarifaECT',
            new_name='idCodigoTarifa',
        ),
    ]
