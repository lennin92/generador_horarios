from django.shortcuts import render
from conf.models import *

# Create your views here.


def por_grado(request):
    diasd = {dia.id:dia for dia in Dia.objects.all()}
    horasd = {hora.id:hora for hora in Hora.objects.all()}
    dias_id = [d for d in diasd]
    horas_id = [d for d in horasd]

    seccionid = request.GET["id"]
    horarios = [h for h in HorarioSeccion.objects.filter(seccion_id=seccionid)]
    horarios_asignacion = {
        (d,h): None for h in horas_id for d in dias_id
    }
    for h in horarios:
        horarios_asignacion[(h.dia.id,h.hora.id)] = h

    return render(request, 'por_grado.html', {
        'dias_id' : dias_id,
        'horas_id' : horas_id,
        'diasd': diasd,
        'horasd': horasd,
        'horarios': horarios,
        'horarios_asignacion': horarios_asignacion
    })
