from django.contrib import admin
from .models import Entrenamiento, EjercicioRealizado, SerieRealizada

# Inline para SerieRealizada
class SerieRealizadaInline(admin.TabularInline):
    model = SerieRealizada
    extra = 1
    ordering = ['ejercicio__nombre']

# Inline para EjercicioRealizado
class EjercicioRealizadoInline(admin.TabularInline):
    model = EjercicioRealizado
    extra = 1
    ordering = ['ejercicio__nombre']

# Configuración del modelo Entrenamiento en el admin
class EntrenamientoAdmin(admin.ModelAdmin):
    inlines = [EjercicioRealizadoInline]  # Anidar EjercicioRealizado
    ordering = ['inicio']

# Registro de modelos
admin.site.register(Entrenamiento, EntrenamientoAdmin)
admin.site.register(EjercicioRealizado)
admin.site.register(SerieRealizada)
