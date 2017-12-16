# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('register','0002_register'),
        ('enrollment','0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoDescuento',
            fields=[
                ('id_tipo_descuento', models.AutoField(primary_key=True, serialize=False)),
                ('colegio', models.ForeignKey(db_column='id_colegio',to='register.Colegio')),
                ('servicio', models.ForeignKey(db_column='id_servicio', to='enrollment.Servicio')),
                ('descripcion', models.CharField(max_length=50)),
                ('porcentaje', models.FloatField()),
                ('fecha_creacion', models.DateField()),
                ('fecha_modificacion', models.DateField()),
                ('usuario_creacion', models.CharField(max_length=10,null=True)),
                ('usuario_modificacion', models.CharField(max_length=10,null=True)),
                ('activo', models.BooleanField()),
            ],
            options={
                #'db_table': 'tipo_descuento',
                'managed': settings.IS_MIGRATE
            },
        ),
        migrations.CreateModel(
            name='Descuento',
            fields=[
                ('id_descuento', models.AutoField(primary_key=True, serialize=False)),
                ('personal_colegio',models.ForeignKey(db_column='id_persona_colegio',to='register.PersonalColegio')),
                ('tipo_descuento', models.ForeignKey(db_column='id_tipo_descuento',to='discounts.TipoDescuento')),
                ('matricula', models.ForeignKey(db_column='id_matricula', to='enrollment.Matricula')),
                ('numero_expediente', models.CharField(max_length=200, null=True)),
                ('estado', models.IntegerField()),
                ('comentario', models.CharField(max_length=200, null=True)),
                ('fecha_solicitud', models.DateField()),
                ('fecha_aprobacion', models.DateField()),
                ('fecha_creacion', models.DateField(null=True, blank=True)),
                ('fecha_modificacion', models.DateField()),
                ('usuario_creacion', models.CharField(max_length=10,null=True)),
                ('usuario_modificacion', models.CharField(max_length=10,null=True)),
                ('activo', models.BooleanField()),
            ],
            options={
                #'db_table': 'descuento',
                'managed': settings.IS_MIGRATE,
                'permissions': (
                    ('aprobar_descuento', 'Para aprobar descuento'),
                    ('detalle_descuento', 'Para ver detalles descuento'),
                    ('Solicitar_Descuento', 'solicitar descuento'),
                    ('Crear_Solicitud', 'crear solicitud'),
                )
            },
        ),
    ]

