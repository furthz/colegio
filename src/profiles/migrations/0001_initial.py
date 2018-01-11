# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        #('register','0002_register'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id_persona', models.AutoField(primary_key=True)),
                ('user', models.OneToOneField(serialize=False,to=settings.AUTH_USER_MODEL, null=True)),
                ('slug', models.UUIDField(default=uuid.uuid4, blank=True, editable=False,null=True)),
                ('picture', models.ImageField(verbose_name='Profile picture', upload_to='profile_pics/%Y-%m-%d/', blank=True, null=True)),
                ('bio', models.CharField(verbose_name='Short Bio', max_length=200, blank=True, null=True)),
                ('email_verified', models.BooleanField(default=False, verbose_name='Email verified')),
                ('nombre', models.CharField(max_length=50)),
                ('segundo_nombre', models.CharField(blank=True, max_length=200, null=True)),
                ('apellido_pa', models.CharField(blank=False, max_length=50, null=False)),
                ('apellido_ma', models.CharField(blank=True, max_length=50, null=True)),
                ('tipo_documento', models.IntegerField(null=True)),
                ('numero_documento', models.CharField(max_length=15, null=True)),
                ('sexo', models.IntegerField(null=True)),
                ('correo', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_nac', models.DateField(null=True)),
                ('usuario_creacion_persona', models.CharField(blank=True, max_length=10, null=True,
                                                              verbose_name='Usuario_Creacion')),
                ('usuario_modificacion_persona', models.CharField(blank=True, max_length=10, null=True,
                                                                  verbose_name='Usuario_Modificacion')),
                ('fecha_creacion_persona', models.DateTimeField(blank=True, null=True)),
                ('fecha_modificacion_persona', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
