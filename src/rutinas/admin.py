from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Rutina, Sesion, EjercicioPersonalizado, SeriePersonalizada

# Define resources for each model
class RutinaResource(resources.ModelResource):
    class Meta:
        model = Rutina

class SesionResource(resources.ModelResource):
    class Meta:
        model = Sesion

class EjercicioPersonalizadoResource(resources.ModelResource):
    class Meta:
        model = EjercicioPersonalizado

class SeriePersonalizadaResource(resources.ModelResource):
    class Meta:
        model = SeriePersonalizada

# Inline para SeriePersonalizada
class SeriePersonalizadaInline(admin.TabularInline):
    model = SeriePersonalizada
    extra = 1
    ordering = ['repeticiones']  # Ordenar por número de repeticiones, por ejemplo

# Inline para EjercicioPersonalizado, con SeriePersonalizada anidado
class EjercicioPersonalizadoInline(admin.TabularInline):
    model = EjercicioPersonalizado
    extra = 1
    inlines = [SeriePersonalizadaInline]
    ordering = ['ejercicio__nombre']  # Ordenar los ejercicios personalizados por nombre

# Inline para Sesion, con EjercicioPersonalizado anidado
class SesionInline(admin.TabularInline):
    model = Sesion
    extra = 1
    inlines = [EjercicioPersonalizadoInline]
    ordering = ['titulo']  # Ordenar las sesiones por título

class RutinaAdmin(ImportExportModelAdmin):
    resource_class = RutinaResource
    inlines = [SesionInline]
    ordering = ['titulo']

class SesionAdmin(ImportExportModelAdmin):
    resource_class = SesionResource

class EjercicioPersonalizadoAdmin(ImportExportModelAdmin):
    resource_class = EjercicioPersonalizadoResource

class SeriePersonalizadaAdmin(ImportExportModelAdmin):
    resource_class = SeriePersonalizadaResource
    list_display = ('__str__',)

# Registramos los modelos
admin.site.register(Rutina, RutinaAdmin)
admin.site.register(Sesion, SesionAdmin)
admin.site.register(EjercicioPersonalizado, EjercicioPersonalizadoAdmin)
admin.site.register(SeriePersonalizada, SeriePersonalizadaAdmin)