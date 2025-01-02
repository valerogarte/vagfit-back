from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from ejercicios.models import Ejercicio


User = get_user_model()

class Rutina(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    imagen = models.ImageField(upload_to='rutinas/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo or 'Sin rutina'

class Sesion(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE, related_name='sesion', null=True, blank=True)
    titulo = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.titulo}' or 'Sin sesión'

class EjercicioPersonalizado(models.Model):
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE, null=True, blank=True)
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE, null=True, blank=True)
    peso_orden = models.FloatField(default=0)

    class Meta:
        ordering = ['peso_orden'] 

    def __str__(self):
        return f'{self.ejercicio.nombre if self.ejercicio else "Sin ejercicio"}'

class SeriePersonalizada(models.Model):
    ejercicio_personalizado = models.ForeignKey(
        EjercicioPersonalizado,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='series'
    )
    repeticiones = models.IntegerField(default=10)
    peso = models.FloatField(default=0)
    velocidad_repeticion = models.FloatField(default=0)
    descanso = models.IntegerField(default=60)
    rer = models.IntegerField(default=0)

    class Meta:
        ordering = ['id']

    def __str__(self):
        rutina = self.ejercicio_personalizado.sesion.rutina.titulo if self.ejercicio_personalizado and self.ejercicio_personalizado.sesion else "Sin rutina"
        sesion = self.ejercicio_personalizado.sesion.titulo if self.ejercicio_personalizado and self.ejercicio_personalizado.sesion else "Sin sesión"
        ejercicio = self.ejercicio_personalizado.ejercicio.nombre if self.ejercicio_personalizado and self.ejercicio_personalizado.ejercicio else "Sin ejercicio"
        return f'{rutina} - {sesion} - {self.id} - {ejercicio}'