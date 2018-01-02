# -*- coding: utf-8 -*-
from django.db import models


class Materia (models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Grado (models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class GradoSeccion (models.Model):
    grado = models.ForeignKey('Grado')
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Docente (models.Model):
    nombre = models.CharField(max_length=50)
    horaEntrada = models.TimeField(blank=True)
    horaSalida = models.TimeField(blank=True)

    def __str__(self):
        return self.nombre


class Dia (models.Model):
    nombre = models.CharField(max_length=25)

    def __str__(self):
        return self.nombre


class Hora (models.Model):
    nombre = models.CharField(max_length=50)
    horaT = models.TimeField(blank=True)
    horaF = models.TimeField(blank=True)

    def __str__(self):
        return self.nombre


class HorarioDocente(models.Model):
    docente = models.ForeignKey('Docente')
    dia = models.ForeignKey('Dia')
    hora = models.ForeignKey('Hora')

    def __str__(self):
        return "%s %s %s"%(self.docente.nombre,
                           self.dia.nombre,
                           self.hora.nombre)

    class Meta:
        unique_together = ("docente", "dia", "hora")


class HorarioSeccion(models.Model):
    seccion = models.ForeignKey('GradoSeccion')
    dia = models.ForeignKey('Dia')
    hora = models.ForeignKey('Hora')

    def __str__(self):
        return "%s %s %s"%(self.seccion.nombre,
                           self.dia.nombre,
                           self.hora.nombre)

    class Meta:
        unique_together = ("seccion", "dia", "hora")


class GeneracionHorarios(models.Model):
    fechaHoraInicio = models.DateTimeField()
    fechaHoraFin = models.DateTimeField()
    TotalDHorasFaltantes = models.IntegerField()
    TotalSHorasFaltantes = models.IntegerField()
    TotalReqPorCumplir   = models.IntegerField()
    observaciones = models.TextField()


class Asignacion(models.Model):
    generacion = models.ForeignKey('GeneracionHorarios')
    materia = models.ForeignKey('Materia')
    gradoSeccion = models.ForeignKey('GradoSeccion')
    docente = models.ForeignKey('Docente')
    dia = models.ForeignKey('Dia')
    hora = models.ForeignKey('Hora')
    horarioDocente = models.ForeignKey('HorarioDocente')
    horarioSeccion= models.ForeignKey('HorarioSeccion')


class RequerimientoGradoMateria(models.Model):
    materia = models.ForeignKey('Materia')
    gradoSeccion = models.ForeignKey('GradoSeccion')
    docente = models.ForeignKey('Docente')
    cantidadHoras = models.IntegerField()

    def __str__(self):
        return "%s %s %s %d"%(self.gradoSeccion.nombre,
                           self.materia.nombre,
                           self.docente.nombre,
                           self.cantidadHoras)

    class Meta:
        unique_together = ("materia", "gradoSeccion")


