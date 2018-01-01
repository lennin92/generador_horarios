from conf.models import *
import datetime


def REQUERIM():
    return  {
        (r.gradoSeccion_id, r.materia_id, r.docente_id):{
            'id': r.id,
            'grado': r.gradoSeccion,
            'materia': r.materia,
            'cantidadHoras': r.cantidadHoras,
            'docente': r.docente,
            'horasCumplidas': 0
        }
        for r in RequerimientoGradoMateria.objects.all()}


def GRADOS():
    return {
        g.id:{
            'id': g.id,
            'horas': {
                (d.dia_id, d.hora_id): None # tupla de tipo (materia_id, grado_id, docente_id)
                    for d in HorarioSeccion.objects.all()
            }
        } for g in GradoSeccion.objects.all()}


def DOCENTES():
    return {
        dc.id:{
            'id':dc.id,
            'horas': {
                (d.dia_id,d.hora_id): None # tupla de tipo (materia_id, grado_id, docente_id)
                    for d in HorarioDocente.objects.all()
            }
        } for dc in Docente.objects.all()}


def es_asignacion_valida(grados, docentes, requerimientos, gra_id, mat_id, prof_id, dia_id, hor_id):
    # validar si el grado está vacio a esa hora
    if gra_id not in grados: return False
    grado = grados[gra_id]
    if grado[(dia_id, hor_id)] is not None: return False

    # validar si el docente tiene libre a esa hora
    if prof_id not in docentes: return False
    docente = docentes[prof_id]
    if docente[(dia_id, hor_id)] is not None: return False

    # validar si el requerimiento ya se cumplio
    req = requerimientos[(gra_id, mat_id, prof_id)]
    if req['horasCumplidas']>=req['cantidadHoras']: return False

    # validad que exista un maximo de 3 horas al dia de una sola materia en el mismo grado
    horas = Hora.objects.all()
    count = 0
    for h in horas:
        hora = grado['horas'][dia_id, h.id]
        if hora is None: continue
        if hora[0] == mat_id: count = count + 1
        if count>=3: return False
    return True


def crear_horario(grados, docentes, requerimientos, grados_ids, docentes_ids, materias_ids, sufl=True):
    gh = GeneracionHorarios()
    gh.fechaHoraInicio = datetime.datetime.now()
    requs = []
    for doc_id in docentes_ids:
        for gra_id in grados_ids:
            for mat_id in materias_ids:
                req = requerimientos[(gra_id, mat_id, doc_id)]
                if req is None: continue
                requs.push((gra_id, mat_id, doc_id))
    if sufl: requs = sorted(requs)
    for r in requs:
        rq = requerimientos[r]
        # while rq['horasCumplidas']<rq['cantidadHoras']:
        mat_id = rq['materia'].id
        prof_id = rq['docente'].id
        gra_id = rq['grado'].id
        for h in docentes[prof_id]['horas']:
            dia_id = h[0]
            hor_id = h[1]
            if es_asignacion_valida(grados, docentes, requerimientos,
                        gra_id, mat_id, prof_id, dia_id, hor_id):
                profesor = docentes[prof_id]
                profesor['horas'][(dia_id, hor_id, )]
                grado = grados[gra_id]
                grado['horas'][(dia_id, hor_id, )]
                rq['horasCumplidas'] = rq['horasCumplidas'] + 1
    # AGREGAR NUEVO GeneracionHorarios
    gh.fechaHoraFin = datetime.datetime.now()
    gh.TotalSHorasFaltantes = 0
    for rk in requerimientos:
        re = requerimientos[rk]
        gh.TotalSHorasFaltantes = gh.TotalSHorasFaltantes + (re['cantidadHoras']-re['horasCumplidas'])
    gh.save()

    # Agregar nuevos Asignacion por cada hora del profe y grado
    for dk in docentes:
        doc = docentes[dk]
        for hk in doc['horas']:
            pass # poner asignacion del docente



