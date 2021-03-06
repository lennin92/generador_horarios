# -*- coding: utf-8 -*-

from django.shortcuts import render
from conf.models import *
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, None)


@register.filter
def dict_tuplegen(d,h):
    return ",".join([str(d),str(h)])


def por_grado(request):
    diasd = {dia.id:dia for dia in Dia.objects.all()}
    horasd = {hora.id:hora for hora in Hora.objects.all()}
    dias_id = [d for d in diasd]
    horas_id = [d for d in horasd]

    seccionid = request.GET["id"]
    seccion = GradoSeccion.objects.filter(id=seccionid)[0]
    if "gen" not in request.GET:
        horarios = [h for h in HorarioSeccion.objects.filter(seccion_id=seccionid)]
        asignado = False
    else:
        genid = request.GET["gen"]
        horarios = [a for a in Asignacion.objects.filter(generacion_id=genid, gradoSeccion_id=seccionid)]
        asignado = True

    horarios_asignacion = {
        ",".join([str(d), str(h)]): '' for h in horas_id for d in dias_id
    }
    for h in horarios:
        horarios_asignacion[",".join([str(h.dia.id), str(h.hora.id)])] = h

    print(horarios)

    return render(request, 'por_grado.html', {
        'dias_id': dias_id,
        'horas_id': horas_id,
        'diasd': diasd,
        'horasd': horasd,
        'horarios': horarios,
        'horarios_asignacion': horarios_asignacion,
        'seccion': seccion,
        'asignado':asignado
    })
