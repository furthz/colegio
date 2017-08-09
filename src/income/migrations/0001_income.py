from django.conf import settings
from django.db import migrations, models



class Migration(migrations.Migration):
    initial = True


    #dependencies = [
    #    (),
    #]

    operations = [

        migrations.CreateModel(
            name='Cobranza',
            fields=[
                ('id_cobranza', models.AutoField(primary_key=True, auto_created=True)),
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
                      'db_table': 'cobranza',
                      'managed': settings.IS_TESTING,
            },
        ),
        migrations.CreateModel(
            name='DetalleCobranza',
            fields=[
                ('id_detalle_cobranza', models.AutoField(primary_key=True, auto_created=True)),
                ('id_cobranza', models.ForeignKey(db_column='id_cobranza', to='income.Cobranza', null=True, blank=True)),
                ('monto', models.FloatField(null=False)),
            ],
            options={
                'db_table': 'detalle_cobranza',
                'managed': settings.IS_TESTING,
            }
        )
    ]
