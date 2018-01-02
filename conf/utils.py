from conf.models import *
from django.utils import timezone
from random import shuffle


def REQUERIM():
    return {
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
            'nombre':g.nombre,
            'horas': {
                (d.dia_id, d.hora_id): None # tupla de tipo (materia_id, grado_id, docente_id)
                    for d in HorarioSeccion.objects.filter(seccion_id=g.id)
            },
            'horaso': {
                (d.dia_id, d.hora_id): d
                    for d in HorarioSeccion.objects.filter(seccion_id=g.id)
            }
        } for g in GradoSeccion.objects.all()}


def DOCENTES():
    return {
        dc.id:{
            'id':dc.id,
            'nombre':dc.nombre,
            'horas': {
                (d.dia_id,d.hora_id): None # tupla de tipo (materia_id, grado_id, docente_id)
                    for d in HorarioDocente.objects.filter(docente_id=dc.id)
            },
            'horaso': {
                (d.dia_id, d.hora_id): d
                    for d in HorarioDocente.objects.filter(docente_id=dc.id)
            }
        } for dc in Docente.objects.all()}


def es_asignacion_valida(grados, docentes, requerimientos, gra_id, mat_id, prof_id, dia_id, hor_id):
    # validar si el grado está vacio a esa hora
    if gra_id not in grados: return False
    grado = grados[gra_id]
    dik = (dia_id, hor_id)
    if dik not in grado['horas']: return False
    if grado['horas'][dik] is not None: return False

    # validar si el docente tiene libre a esa hora
    if prof_id not in docentes: return False
    docente = docentes[prof_id]
    if dik not in docente['horas']: return False
    if docente['horas'][dik] is not None: return False

    # validar si el requerimiento ya se cumplio
    # print("validar si el requerimiento ya se cumplio")
    req = requerimientos[(gra_id, mat_id, prof_id)]
    if req['horasCumplidas']>=req['cantidadHoras']: return False

    # validar que exista un maximo de 3 horas al dia de una sola materia en el mismo grado
    #print("validar que exista un maximo de 3 horas al dia de una sola materia en el mismo grado")
    horas = Hora.objects.all()
    count = 0
    for h in horas:
        k = (dia_id, h.id,)
        if k not in grado['horas']: continue
        hora = grado['horas'][k]
        if hora is None: continue
        if hora[0] == mat_id: count = count + 1
        if count>=3: return False
    return True


def crear_horario(grados, docentes, requerimientos, grados_ids, docentes_ids, materias_ids, sufl=True):
    gh = GeneracionHorarios()
    gh.fechaHoraInicio = timezone.now()
    requs = []
    for doc_id in docentes_ids:
        for gra_id in grados_ids:
            for mat_id in materias_ids:
                k = (gra_id, mat_id, doc_id)
                if k not in requerimientos: continue
                req = requerimientos[k]
                if req is None: continue
                requs.append(k)
    if sufl: shuffle(requs)
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
                profesor['horas'][(dia_id, hor_id, )] = (mat_id, gra_id, prof_id,)# tupla de tipo (materia_id, grado_id, docente_id)
                grado = grados[gra_id]
                grado['horas'][(dia_id, hor_id, )] = (mat_id, gra_id, prof_id,)
                rq['horasCumplidas'] = rq['horasCumplidas'] + 1
    # AGREGAR NUEVO GeneracionHorarios
    gh.fechaHoraFin = timezone.now()
    gh.TotalSHorasFaltantes = 0
    gh.TotalDHorasFaltantes = 0
    gh.TotalReqPorCumplir = 0
    gh.observaciones = ''
    count = 0
    for rk in requerimientos:
        re = requerimientos[rk]
        falt = re['cantidadHoras']-re['horasCumplidas']
        if falt>0:
            count += 1
            gh.TotalSHorasFaltantes = gh.TotalSHorasFaltantes + (falt)
            gh.observaciones += 'Faltan %d horas en %s %s %s %d;'%(falt, re['grado'].nombre,
                                                                  re['docente'].nombre, re['materia'].nombre,
                                                                  re['cantidadHoras'])
    gh.TotalReqPorCumplir = count
    gh.save()

    # Agregar nuevos Asignacion por cada hora del profe y grado
    for dk in docentes:
        doc = docentes[dk]
        # print(doc)
        for hk in doc['horas']:
            ht = doc['horas'][hk]
            if ht is None: continue
            # poner asignacion del docente
            hdo = doc['horaso'][hk]
            mk = ht[0] # tupla con esquema(materia_id, seccion_id, docente_id)
            sk = ht[1] # tupla con esquema(materia_id, seccion_id, docente_id)
            dck = ht[2] # tupla con esquema(materia_id, seccion_id, docente_id)
            hso = grados[sk]['horaso'][hk]
            a = Asignacion()
            a.generacion = gh
            a.materia_id = mk
            a.gradoSeccion_id = sk
            a.docente_id = dck
            a.dia_id = hk[0]# tupla con esquema(dia_id, hora_id)
            a.hora_id = hk[1]# tupla con esquema(dia_id, hora_id)
            a.horarioDocente = hdo
            a.horarioSeccion = hso
            a.save()


def run():
    count = 1
    print("Corrida %d"%(count, ))
    grados = GRADOS()
    docentes= DOCENTES()
    requerimientos = REQUERIM()
    grados_ids = [d.id for d in GradoSeccion.objects.all()]
    docentes_ids = [d.id for d in Docente.objects.all()]
    materias_ids = [d.id for d in Materia.objects.all()]
    crear_horario(grados, docentes, requerimientos, grados_ids, docentes_ids, materias_ids, False)
    count += 1
    print("Corrida %d"%(count, ))
    grados = GRADOS()
    docentes= DOCENTES()
    requerimientos = REQUERIM()
    grados_ids = [d.id for d in GradoSeccion.objects.all()]
    docentes_ids = [d.id for d in Docente.objects.all()]
    materias_ids = [d.id for d in Materia.objects.all()]
    crear_horario(grados, docentes, requerimientos, grados_ids, docentes_ids, materias_ids, True)
    for i in range(70):
        count+=1
        print("Corrida %d"%(count, ))
        grados = GRADOS()
        docentes = DOCENTES()
        requerimientos = REQUERIM()
        grados_ids = [d.id for d in GradoSeccion.objects.all()]
        docentes_ids = [d.id for d in Docente.objects.all()]
        materias_ids = [d.id for d in Materia.objects.all()]
        shuffle(grados_ids)
        shuffle(docentes_ids)
        shuffle(materias_ids)
        crear_horario(grados, docentes, requerimientos, grados_ids, docentes_ids, materias_ids, True)


run()




