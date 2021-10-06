# Generated by Django 3.2.5 on 2021-07-06 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TT_codigoTarifaECT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigoECT', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='TT_tarifaECT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peso', models.CharField(max_length=20)),
                ('rangeL1', models.CharField(max_length=20)),
                ('rangeL2', models.CharField(max_length=20)),
                ('rangeL3', models.CharField(max_length=20)),
                ('rangeL4', models.CharField(max_length=20)),
                ('rangeE1', models.CharField(max_length=20)),
                ('rangeE2', models.CharField(max_length=20)),
                ('rangeE3', models.CharField(max_length=20)),
                ('rangeE4', models.CharField(max_length=20)),
                ('rangeN1', models.CharField(max_length=20)),
                ('rangeN2', models.CharField(max_length=20)),
                ('rangeN3', models.CharField(max_length=20)),
                ('rangeN4', models.CharField(max_length=20)),
                ('rangeN5', models.CharField(max_length=20)),
                ('rangeN6', models.CharField(max_length=20)),
                ('rangeI1', models.CharField(max_length=20)),
                ('rangeI2', models.CharField(max_length=20)),
                ('rangeI3', models.CharField(max_length=20)),
                ('rangeI4', models.CharField(max_length=20)),
                ('rangeI5', models.CharField(max_length=20)),
                ('rangeI6', models.CharField(max_length=20)),
                ('idTT_tarifaECT', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='controleTarifaECT.tt_codigotarifaect')),
            ],
        ),
    ]