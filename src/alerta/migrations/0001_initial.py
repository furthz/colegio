# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-22 20:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from profiles.models import BaseProfile


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoAlerta',
            fields=[
                ('id_tipo_alerta', models.AutoField(primary_key=True)),
                ('descripcion', models.CharField(max_length=100, blank=True, null=True)),
                ('activo', models.BooleanField()),
                ('fecha_creacion', models.DateTimeField(blank=True, null=True)),
                ('fecha_modificacion', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                # 'db_table': 'tipo_servicio',
                'managed': settings.IS_MIGRATE,
                # 'managed': False,

            },
        ),
        migrations.CreateModel(
            name='EstadoAlerta',
            fields=[
                ('id_estado_alerta', models.AutoField(primary_key=True)),
                ('descripcion', models.CharField(max_length=100, blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(blank=True, null=True)),
                ('fecha_modificacion', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                # 'db_table': 'servicio',
                'managed': settings.IS_MIGRATE,
                # 'managed': False,

            },
        ),
        migrations.CreateModel(
            name='ContenidoAlerta',
            fields=[
                ('id_contenido_alerta', models.AutoField(primary_key=True)),
                ('contenido', models.CharField(max_length=10000, blank=True, null=True)),
            ],
            options={
                # 'db_table': 'matricula',
                'managed': settings.IS_MIGRATE,
                # 'managed': False,

            },
        ),
        migrations.CreateModel(
            name='Alerta',
            fields=[
                ('id_alerta', models.AutoField(primary_key=True)),
                ('matricula', models.ForeignKey(db_column='id_matricula', to='enrollment.Matricula', blank=True, null=True)),
                ('persona_emisor', models.ForeignKey(db_column='id_persona_emisor', to='profiles.PersonaEmisor')),
                ('persona_receptor', models.ForeignKey(db_column='id_persona_receptor', to='profiles.PersonaReceptor')),
                ('tipo_alerta', models.ForeignKey(db_column='id_tipo_alerta', to='alerta.TipoAlerta')),
                ('estado_alerta', models.ForeignKey(db_column='id_estado_alerta', to='alerta.EstadoAlerta')),
                ('contenido_alerta', models.ForeignKey(db_column='id_contenido_alerta', to='alerta.ContenidoAlerta')),
                ('img_url_alertas', models.CharField(max_length=10000, blank=True, null=True)),
                ('fecha_visto', models.DateTimeField(blank=True, null=True)),
                ('visto', models.IntegerField()),
                ('fecha_creacion', models.DateTimeField(blank=True, null=True)),
                ('fecha_modificacion', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                # 'db_table': 'matricula',
                'managed': settings.IS_MIGRATE,
                # 'managed': False,

            },
        ),
    ]
