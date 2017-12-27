# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conf', '0006_auto_20171224_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneracionHorarios',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fechaHoraInicio', models.DateTimeField()),
                ('fechaHoraFin', models.DateTimeField()),
                ('TotalDHorasFaltantes', models.IntegerField()),
                ('TotalSHorasFaltantes', models.IntegerField()),
                ('TotalReqPorCumplir', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RequerimientoGradoMateria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidadHoras', models.IntegerField()),
                ('docente', models.ForeignKey(to='conf.Docente')),
                ('gradoSeccion', models.ForeignKey(to='conf.GradoSeccion')),
                ('materia', models.ForeignKey(to='conf.Materia')),
            ],
        ),
        migrations.AlterField(
            model_name='asignacion',
            name='horarioDocente',
            field=models.ForeignKey(to='conf.HorarioDocente'),
        ),
        migrations.AlterField(
            model_name='asignacion',
            name='horarioSeccion',
            field=models.ForeignKey(to='conf.HorarioSeccion'),
        ),
        migrations.AddField(
            model_name='asignacion',
            name='generacion',
            field=models.ForeignKey(default=1, to='conf.GeneracionHorarios'),
            preserve_default=False,
        ),
    ]
