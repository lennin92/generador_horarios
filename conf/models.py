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


class HorarioSeccion(models.Model):
    seccion = models.ForeignKey('GradoSeccion')
    dia = models.ForeignKey('Dia')
    hora = models.ForeignKey('Hora')

    def __str__(self):
        return "%s %s %s"%(self.seccion.nombre,
                           self.dia.nombre,
                           self.hora.nombre)

class Asignacion(models.Model):
    materia = models.ForeignKey('Materia')
    gradoSeccion = models.ForeignKey('GradoSeccion')
    docente = models.ForeignKey('Docente')
    dia = models.ForeignKey('Dia')
    hora = models.ForeignKey('Hora')
    horarioDocente = models.OneToOneField('HorarioDocente')
    horarioSeccion= models.OneToOneField('HorarioSeccion')
