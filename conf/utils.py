from conf.models import *

GRADOS = {
    g.id:{
        'id' : g.id,
        'materias': {
            rm.materia.id: {
                'id': rm.materia.id,
                'asignadas':0,
                'requeridas': rm.cantidadHoras,
                'docente': rm.docente,
                'docente_id': rm.docente_id,
                'asignaciones':[]
            } for rm in RequerimientoGradoMateria.objects.filter(gradoSeccion_id=g.id)
        }
    } for g in GradoSeccion.objects.all()}


def is_valid_asignation(grados, gra_id, mat_id, dia_id, hor_id, prof_id):
    if gra_id not in grados: return False
    grado = grados[gra_id]
    if mat_id not in grado['materias']: return False
    return True