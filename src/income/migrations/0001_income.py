from django.conf import settings
from django.db import migrations, models



class Migration(migrations.Migration):
    initial = True


    dependencies = [
        ('cash','0001_initial'),
        ('enrollment','0001_initial'),
    ]

    operations = [

        migrations.CreateModel(
            name='Cobranza',
            fields=[
                ('id_cobranza', models.AutoField(primary_key=True, auto_created=True)),
                ('movimiento',models.ForeignKey(to='cash.CajaCajero', db_column='id_movimiento')),
                ('fecha_pago', models.DateField(null=False)),
                ('fecha_creacion', models.DateField(null=True)),
                ('fecha_modificacion', models.DateField(null=True)),
                ('monto', models.FloatField(null=False)),
                ('comentario', models.CharField(max_length=500, null=True)),
                ('medio_pago', models.IntegerField(null=True)),
                ('num_operacion', models.IntegerField(null=True)),
                ('usuario_creacion', models.CharField(max_length=10, null=True)),
                ('usuario_modificacion', models.CharField(max_length=10, null=True)),
            ],
            options = {
                      #'db_table': 'cobranza',
                      'managed': settings.IS_MIGRATE,

            },
        ),
        migrations.CreateModel(
            name='DetalleCobranza',
            fields=[
                ('id_detalle_cobranza', models.AutoField(primary_key=True, auto_created=True)),
                ('id_cobranza', models.ForeignKey(db_column='id_cobranza', to='income.Cobranza', null=True, blank=True)),
                ('cuentascobrar',models.ForeignKey(db_column='id_cuentascobrar', to = 'enrollment.Cuentascobrar')),
                ('monto', models.FloatField(null=False)),
            ],
            options={
                #'db_table': 'detalle_cobranza',
                'managed': settings.IS_MIGRATE,
            }
        )
    ]
