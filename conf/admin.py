from django.contrib import admin
from conf.models import *

admin.site.register(Materia)
admin.site.register(Grado)
admin.site.register(GradoSeccion)
admin.site.register(Docente)
admin.site.register(Dia)
admin.site.register(Hora)
admin.site.register(Asignacion)


class HorarioDocenteAdmin(admin.ModelAdmin):
    list_display = ('docente', 'dia', 'hora')

admin.site.register(HorarioDocente, HorarioDocenteAdmin)


class HorarioSeccionAdmin(admin.ModelAdmin):
    list_display = ('seccion', 'dia', 'hora')

admin.site.register(HorarioSeccion, HorarioSeccionAdmin)


class RequerimientoGradoMateriaAdmin(admin.ModelAdmin):
    list_display = ('materia', 'docente', 'gradoSeccion', 'cantidadHoras')

admin.site.register(RequerimientoGradoMateria, RequerimientoGradoMateriaAdmin)