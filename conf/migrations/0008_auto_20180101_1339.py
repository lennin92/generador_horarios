# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-01 19:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conf', '0007_auto_20171227_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='generacionhorarios',
            name='observaciones',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='horariodocente',
            unique_together=set([('docente', 'dia', 'hora')]),
        ),
        migrations.AlterUniqueTogether(
            name='horarioseccion',
            unique_together=set([('seccion', 'dia', 'hora')]),
        ),
        migrations.AlterUniqueTogether(
            name='requerimientogradomateria',
            unique_together=set([('materia', 'gradoSeccion')]),
        ),
    ]
